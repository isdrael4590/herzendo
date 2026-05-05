"""
Extractor de datos médicos desde PDF.

Estrategia en dos capas:
  1. PyMuPDF  → extracción de texto rápida y eficiente en memoria (archivos grandes)
  2. pdfplumber → extracción de tablas de laboratorio (más precisa para valores numéricos)

Codebook detectado en los datos reales:
  1 / "1. SI"  → si
  2 / "2. NO"  → no
  4 / "NO DATO" / "NO APLICA" → (vacío)
  Interpretaciones: 1=Normal, 2=Elevado, 3=Bajo, 4=No determinado
"""

import re
import io

# ── Mapa hormonas → campos del modelo ────────────────────────────────────────
# (patrón_nombre, campo_valor)
MAPA_HORMONAS = [
    (r'GH\b|Hormona.{0,8}Crec',   'gh'),
    (r'IGF.?1|Somatomedina',       'igf1'),
    (r'\bLH\b|Luteinizante',       'lh'),
    (r'\bFSH\b|Folículo|Foliculo', 'fsh'),
    (r'Estradiol|E2\b',            'estradiol'),
    (r'Testosterona',               'testosterona'),
    (r'\bTSH\b|Tirotropina',       'tsh'),
    (r'T4.{0,5}(libre|L\b|Free)',  't4l'),
    (r'Cortisol',                   'cortisol'),
    (r'\bACTH\b|Corticotrop',      'acth'),
    (r'Prolactina|PRL\b',          'prolactina'),
    (r'Ki.?67',                     'ki67'),
]

# ── Palabras clave que indican páginas con datos clínicos ─────────────────────
KEYWORDS_LAB = re.compile(
    r'GH|IGF|TSH|ACTH|Prolactina|Cortisol|Testosterona|Estradiol|LH\b|FSH\b|Ki.67',
    re.IGNORECASE
)


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN DE TEXTO
# ═══════════════════════════════════════════════════════════════════════════════

def extraer_texto(archivo) -> str:
    """
    Usa PyMuPDF cuando está disponible (eficiente en RAM para PDFs grandes).
    Fallback a pdfplumber.
    """
    contenido = archivo.read()
    try:
        return _texto_pymupdf(contenido)
    except Exception:
        return _texto_pdfplumber(io.BytesIO(contenido))


def _texto_pymupdf(contenido: bytes) -> str:
    import fitz  # PyMuPDF
    doc = fitz.open(stream=contenido, filetype='pdf')
    paginas = []
    for pag in doc:
        t = pag.get_text('text')
        if t and t.strip():
            paginas.append(t)
    doc.close()
    return '\n'.join(paginas)


def _texto_pdfplumber(fuente) -> str:
    import pdfplumber
    paginas = []
    with pdfplumber.open(fuente) as pdf:
        for pag in pdf.pages:
            t = pag.extract_text()
            if t:
                paginas.append(t)
    return '\n'.join(paginas)


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN DE TABLAS  (solo páginas con palabras clave para no ralentizar)
# ═══════════════════════════════════════════════════════════════════════════════

def extraer_tablas(archivo_bytes: bytes) -> list[list[list[str]]]:
    """Devuelve todas las tablas encontradas en páginas con datos de laboratorio."""
    import pdfplumber
    tablas = []
    try:
        with pdfplumber.open(io.BytesIO(archivo_bytes)) as pdf:
            for pag in pdf.pages:
                texto_pag = pag.extract_text() or ''
                if not KEYWORDS_LAB.search(texto_pag):
                    continue
                for tbl in pag.extract_tables() or []:
                    if tbl and len(tbl) > 1:
                        tablas.append(tbl)
    except Exception:
        pass
    return tablas


# ═══════════════════════════════════════════════════════════════════════════════
# NORMALIZACIÓN DE VALORES DEL CODEBOOK
# ═══════════════════════════════════════════════════════════════════════════════

_RE_NUMERO = re.compile(r'[Oo](\.\d)', )   # letra O confundida con 0

def _limpiar_num(valor: str) -> str:
    """Normaliza número: '0,54' → '0.54', 'O.54' → '0.54'"""
    v = str(valor).strip()
    v = _RE_NUMERO.sub(r'0\1', v)       # O.54 → 0.54
    v = v.replace(',', '.')             # 0,54 → 0.54
    return v if re.match(r'^-?\d+(\.\d+)?$', v) else ''


def _es_vacio(valor: str) -> bool:
    """Detecta los marcadores de 'sin dato' del codebook."""
    v = str(valor).strip().upper()
    return v in ('', 'NO DATO', 'NO APLICA', 'ND', 'N/A', 'NA', 'NO DATA',
                 'NO DETERMINADO', 'SIN DATO', '-', '—')


def _decodificar_sino(valor: str) -> str:
    """Convierte '1', '1. SI', 'SI', '2', '2. No', 'NO' → 'si'/'no'/''"""
    v = str(valor).strip()
    if _es_vacio(v):
        return ''
    # Extraer solo el texto después del número inicial: "1. SI" → "SI"
    m = re.match(r'^\d+\.\s*(.+)$', v)
    if m:
        v = m.group(1).strip()
    v_u = v.upper()
    if v_u in ('1', 'SI', 'SÍ', 'S', 'YES', 'Y'):
        return 'si'
    if v_u in ('2', 'NO', 'N'):
        return 'no'
    return ''


def _decodificar_interp(valor: str) -> str:
    """Convierte '1'=Normal, '2'=Elevado/'Elevada', '3'=Bajo, '4'=No det."""
    v = str(valor).strip()
    if _es_vacio(v):
        return ''
    m = re.match(r'^(\d+)', v)
    codigo = m.group(1) if m else v.upper()
    return {
        '1': 'normal', 'NORMAL': 'normal',
        '2': 'elevado', 'ELEVADO': 'elevado', 'ELEVADA': 'elevado', 'ALTO': 'elevado',
        '3': 'bajo',    'BAJO': 'bajo',   'BAJA': 'bajo',
        '4': 'no_det',  'NO_DET': 'no_det', 'NO DETERMINADO': 'no_det',
    }.get(codigo.upper(), '')


def _extraer_numero_de_texto(celda: str) -> str:
    """Extrae el primer número de una celda (ej: '25,3 ng/mL' → '25.3')."""
    if _es_vacio(celda):
        return ''
    # Primero limpiar letra O confundida con cero
    celda = _RE_NUMERO.sub(r'0\1', celda)
    m = re.search(r'-?\d+[.,]\d+|-?\d+', celda)
    if m:
        return m.group().replace(',', '.')
    return ''



# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN DESDE TABLAS DE LABORATORIO
# ═══════════════════════════════════════════════════════════════════════════════

def _indice_columna(cabeceras: list[str], patrones: list[str]) -> int:
    for i, h in enumerate(cabeceras):
        for p in patrones:
            if re.search(p, str(h), re.IGNORECASE):
                return i
    return -1


def campos_de_tablas(tablas: list) -> dict:
    """
    Busca en tablas de pdfplumber filas con nombres de hormonas y extrae:
      valor, ref_min, ref_max, interpretación.
    """
    resultado = {}

    for tabla in tablas:
        filas = [[str(c or '').strip() for c in fila] for fila in tabla]
        if not filas:
            continue

        cabeceras = filas[0]

        idx_val = _indice_columna(cabeceras, [r'resultado|valor|result|value'])
        if idx_val < 0 and len(cabeceras) >= 2:
            idx_val = 1

        for fila in filas[1:]:
            if not fila or not fila[0]:
                continue
            nombre_celda = fila[0]

            for patron, c_val in MAPA_HORMONAS:
                if not re.search(patron, nombre_celda, re.IGNORECASE):
                    continue
                if c_val and idx_val >= 0 and idx_val < len(fila):
                    v = _extraer_numero_de_texto(fila[idx_val])
                    if v:
                        resultado[c_val] = v
                break

    return resultado


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN DESDE TEXTO LIBRE (con conocimiento del codebook)
# ═══════════════════════════════════════════════════════════════════════════════

def _buscar(patron, texto, grupo=1):
    m = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
    return m.group(grupo).strip() if m else ''


def _num_texto(patron, texto) -> str:
    val = _buscar(patron, texto)
    return _limpiar_num(val) if val else ''


def campos_de_texto(texto: str) -> dict:
    d = {}

    # ── Datos generales ───────────────────────────────────────────────────────
    for p in [
        # MSP: "HISTORIA CLÍNICA No. HCU 1805742051 -- DELIA ESTEFANIA MALIZA TOALOMBO"
        r'HCU\s+[\d]+\s+--\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{4,70})',
        # MSP: campo "Empresa: DELIA ESTEFANIA MALIZA TOALOMBO"
        r'Empresa[:\s]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{4,70})',
        # Otros formatos genéricos
        r'(?:Paciente|Nombre completo|Nombre y apellidos?|Nombres?)[:\s]+([A-ZÁÉÍÓÚÑ][^\n]{2,70})',
        r'^([A-ZÁÉÍÓÚÑ]{2,}(?:\s+[A-ZÁÉÍÓÚÑ]{2,}){1,4})\s*$',
    ]:
        v = _buscar(p, texto)
        if v and len(v.strip()) > 4:
            d['nombre'] = v.strip(); break

    # Prioridad 1: código de barras grande  "*1805742051"
    _hcu_raw = _buscar(r'\*(\d{6,})', texto)
    # Prioridad 2: encabezado "HISTORIA CLÍNICA No. HCU 1805742051"
    if not _hcu_raw:
        _hcu_raw = _buscar(
            r'(?:Historia\s+Cl[ií]nica\s+No\.?\s*H?C?U?'
            r'|H\.?C\.?U\.?'
            r'|N[°º#]\s*(?:historia|paciente|HC)'
            r')[:\s#\.]*(\d{4,})',
            texto)
    d['hcu'] = _hcu_raw if _hcu_raw else None
    d['edad_diagnostico'] = _num_texto(
        r'(?:Edad al diagn[oó]stico|Edad)[:\s]+(\d+(?:[.,]\d+)?)\s*(?:años|a[ñn]os|a\.)?', texto)
    d['cirujano'] = _buscar(
        r'(?:Cirujano|Operado por|M[eé]dico tratante|Dr\.?)[:\s]+([A-ZÁÉÍÓÚÑ][^\n]{4,60})', texto)
    d['procedimiento'] = _buscar(
        r'(?:Procedimiento|Intervenci[oó]n quirúrgica?)[:\s]+([^\n]{5,150})', texto)
    d['tipo_histologico'] = _buscar(
        r'(?:Tipo histol[oó]gico|Histolog[ií]a|Diagnóstico histol)[:\s]+([^\n]{3,120})', texto)
    d['hormonas_ihq'] = _buscar(
        r'(?:Hormonas?\s*IHQ|Inmunohistoqu[ií]mica)[:\s]+([^\n]{3,200})', texto)
    d['descripcion_ihq'] = _buscar(
        r'(?:Descripci[oó]n\s*IHQ|Describe[:\s]*hormonas?)[:\s]+([^\n]{3,300})', texto)

    sexo_raw = _buscar(r'(?:Sexo|G[eé]nero)[:\s]+(Masculino|Femenino|\bM\b|\bF\b|Hombre|Mujer)', texto)
    if re.search(r'Masculino|Hombre|\bM\b', sexo_raw, re.I):
        d['sexo'] = 'M'
    elif re.search(r'Femenino|Mujer|\bF\b', sexo_raw, re.I):
        d['sexo'] = 'F'

    d['pais_nacimiento'] = _buscar(
        r'(?:Pa[ií]s de nacimiento|Nacionalidad)[:\s]+([^\n]{2,60})', texto)

    # ── Fecha del procedimiento ───────────────────────────────────────────────
    if not d.get('fecha_procedimiento'):
        fecha_raw = _buscar(
            r'Fecha\s*(?:Nac[i.]?|Nacimiento|procedimiento|cirug[ií]a)?[:\s]+(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})',
            texto)
        if fecha_raw:
            import re as _re
            m = _re.match(r'(\d{2})/(\d{2})/(\d{4})', fecha_raw)
            if m:
                d['fecha_procedimiento'] = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            else:
                d['fecha_procedimiento'] = fecha_raw

    # ── Etnia ─────────────────────────────────────────────────────────────────
    etnia_raw = _buscar(r'(?:Etnia|Grupo\s+[eé]tnico)[:\s]+([^\n]{2,40})', texto)
    if etnia_raw:
        e = etnia_raw.strip().lower()
        if   'mestiz' in e:                                       d['etnia'] = 'mestizo'
        elif any(x in e for x in ('achuar','indigena','indígena','kichwa','shuar')): d['etnia'] = 'indigena'
        elif 'afro' in e:                                         d['etnia'] = 'afroecuatoriano'
        elif 'blanc' in e:                                        d['etnia'] = 'blanco'
        elif 'montubi' in e or 'montuvio' in e:                   d['etnia'] = 'montubio'
        else:                                                     d['etnia'] = 'otro'

    # ── Nivel de instrucción ──────────────────────────────────────────────────
    niv_raw = _buscar(r'(?:Nivel\s+Educativo|Instrucci[oó]n|Escolaridad)[:\s]+([^\n]{2,60})', texto)
    if niv_raw:
        n = niv_raw.strip().lower()
        if   'no aplica' in n or 'ninguna' in n:              d['nivel_instruccion'] = 'ninguna'
        elif 'primaria' in n and 'incompleta' in n:           d['nivel_instruccion'] = 'primaria_incompleta'
        elif 'primaria' in n:                                  d['nivel_instruccion'] = 'primaria_completa'
        elif 'secundaria' in n and 'incompleta' in n:         d['nivel_instruccion'] = 'secundaria_incompleta'
        elif 'secundaria' in n or 'bachillerato' in n:        d['nivel_instruccion'] = 'secundaria_completa'
        elif 'superior' in n and 'incompleta' in n:           d['nivel_instruccion'] = 'superior_incompleta'
        elif 'superior' in n or 'universit' in n:             d['nivel_instruccion'] = 'superior_completa'

    # ── Provincia de nacimiento (Departamento en el PDF) ─────────────────────
    PROVINCIAS_EC = [
        'Azuay','Bolívar','Cañar','Carchi','Chimborazo','Cotopaxi','El Oro',
        'Esmeraldas','Galápagos','Guayas','Imbabura','Loja','Los Ríos','Manabí',
        'Morona Santiago','Napo','Orellana','Pastaza','Pichincha','Santa Elena',
        'Santo Domingo','Sucumbíos','Tungurahua','Zamora Chinchipe',
    ]
    prov_raw = _buscar(r'(?:Departamento|Provincia)[:\s]+([^\n]{2,50})', texto)
    if prov_raw:
        pr = prov_raw.strip()
        match = next((p for p in PROVINCIAS_EC if p.lower() in pr.lower()), None)
        if match:
            d['provincia_nacimiento'] = match

    # ── Hormonas – texto libre ────────────────────────────────────────────────
    for patron, c_val in MAPA_HORMONAS:
        v = _num_texto(
            rf'(?:{patron})[:\s]+(-?\d+[.,]?\d*)\s*(?:ng|mU|µg|ug|pg|nmol|pmol|µUI|mUI|UI)?(?:/\w+)?',
            texto)
        if v and c_val:
            d[c_val] = v

    # ── Tumor ─────────────────────────────────────────────────────────────────
    # Formato "29X37X29 MM" o "29x37 mm" o solo "10 mm"
    m_tam = re.search(
        r'(\d+[.,]?\d*)\s*[xX×]\s*(\d+[.,]?\d*)(?:\s*[xX×]\s*(\d+[.,]?\d*))?\s*mm',
        texto, re.IGNORECASE)
    if m_tam:
        dims = [g for g in m_tam.groups() if g]
        d['tamano_tumor'] = _limpiar_num(max(dims, key=lambda x: float(x.replace(',', '.'))))
    else:
        v = _num_texto(r'(?:Tama[ñn]o|Diámetro)[^\n]*?(\d+[.,]?\d*)\s*mm', texto)
        if v:
            d['tamano_tumor'] = v

    knosp = _buscar(r'KNOSP\s*[:\s]?([0-4])', texto)
    if knosp:
        d['knosp'] = knosp

    v = _num_texto(r'Ki[\s\-]?67[:\s]+(\d+[.,]?\d*)\s*%?', texto)
    if v:
        d['ki67'] = v
        try:
            pct = float(v)
            if   pct < 1:   d['ki67_interp'] = 'muy_bajo'
            elif pct <= 3:  d['ki67_interp'] = 'bajo'
            elif pct <= 10: d['ki67_interp'] = 'alto'
            else:           d['ki67_interp'] = 'muy_alto'
        except ValueError:
            pass

    # ── Síntomas (texto libre) ────────────────────────────────────────────────
    pares_sintomas = [
        ('cefalea',            r'Cefalea[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('apoplejia',          r'Apoplej[ií]a[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('convulsiones',       r'Convulsiones[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('alt_campo_visual',   r'Campo visual[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('deficit_vasopresina',r'Vasopresina[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('acromegalia',        r'Acromegalia[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('cushing',            r'Cushing[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('amenorrea',          r'Amenorrea[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
        ('hipotiroidismo_central', r'Hipotiroidismo central[:\s]+(S[ií]|No|\b1\b|\b2\b)'),
    ]
    for campo, pat in pares_sintomas:
        v = _buscar(pat, texto)
        if v:
            dec = _decodificar_sino(v)
            if dec:
                d[campo] = dec

    return {k: v for k, v in d.items() if v}


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN CON GEMINI
# ═══════════════════════════════════════════════════════════════════════════════

_CAMPOS_VALIDOS = {
    'nombre','hcu','edad_diagnostico','sexo','fecha_procedimiento','etnia',
    'nivel_instruccion','provincia_nacimiento','pais_nacimiento',
    'procedimiento','cirujano','primera_cirugia','solo_biopsia',
    'extranjero','antecedentes_fam','detalle_sindrome',
    'gh','igf1','lh','fsh','estradiol','testosterona',
    'tsh','t4l','cortisol','acth','prolactina','ki67',
    'acromegalia','cushing','hipotiroidismo_central','tirotropinoma',
    'deficit_vasopresina','apoplejia','cefalea','alt_campo_visual',
    'convulsiones','fistula_lcr','sind_seno_cavernoso',
    'tamano_tumor','invasion_seno_cav','knosp','tipo_histologico',
    'reticulina_distorsionada','hormonas_ihq','descripcion_ihq',
    'ki67_interp','observaciones',
}

_PROMPT_GEMINI = """
Eres un asistente médico especializado en registros clínicos de pacientes con tumores hipofisarios.
Analiza el texto de historial médico y extrae los campos listados.

REGLAS ESTRICTAS:
- Responde ÚNICAMENTE con un objeto JSON válido. Sin texto adicional, sin bloques markdown.
- Incluye solo los campos que encuentres claramente en el texto.
- Valores numéricos (hormonas, edad, tamaño tumor, Ki-67): número como string con punto decimal. Ej: "25.3"
- Campos si/no (acromegalia, cushing, cefalea, etc.): exactamente "si" o "no"
- fecha_procedimiento: formato YYYY-MM-DD
- sexo: "M" o "F"
- etnia: mestizo | indigena | afroecuatoriano | blanco | montubio | otro
- nivel_instruccion: ninguna | primaria_completa | primaria_incompleta | secundaria_completa | secundaria_incompleta | superior_completa | superior_incompleta
- tipo_histologico: prolactinoma | somatotropinoma | corticotropinoma | gonadotropinoma | tirotropinoma | carcinoma
- knosp: 0 | 1 | 2 | 3 | 4

CAMPOS A EXTRAER:
nombre, hcu, edad_diagnostico, sexo, fecha_procedimiento, etnia, nivel_instruccion,
provincia_nacimiento, pais_nacimiento, procedimiento, cirujano,
primera_cirugia, solo_biopsia, extranjero, antecedentes_fam,
gh, igf1, lh, fsh, estradiol, testosterona, tsh, t4l, cortisol, acth, prolactina, ki67,
acromegalia, cushing, hipotiroidismo_central, tirotropinoma,
deficit_vasopresina, apoplejia, cefalea, alt_campo_visual,
convulsiones, fistula_lcr, sind_seno_cavernoso,
tamano_tumor, invasion_seno_cav, knosp, tipo_histologico,
reticulina_distorsionada, hormonas_ihq, descripcion_ihq, ki67_interp, observaciones

TEXTO DEL HISTORIAL:
{texto}
"""

def campos_de_gemini(texto: str) -> tuple[dict, str]:
    """
    Llama a Gemini para extraer campos.
    Devuelve (campos_dict, status_msg).
    status_msg: 'ok:<modelo>' | 'sin_key' | 'error:<detalle>'
    """
    import os, json
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not api_key:
        return {}, 'sin_key'

    modelo = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(modelo)

        texto_recortado = texto[:12_000]
        prompt = _PROMPT_GEMINI.format(texto=texto_recortado)

        resp = model.generate_content(
            prompt,
            generation_config={'temperature': 0, 'max_output_tokens': 1024},
        )
        raw = resp.text.strip()

        # Extraer el objeto JSON de la respuesta (Gemini puede añadir texto antes/después)
        inicio = raw.find('{')
        fin    = raw.rfind('}')
        if inicio == -1 or fin == -1 or fin <= inicio:
            return {}, f'error:no se encontró JSON en la respuesta'
        raw = raw[inicio:fin + 1]

        data = json.loads(raw)
        if not isinstance(data, dict):
            return {}, f'error:respuesta no es JSON objeto'

        campos = {k: str(v).strip() for k, v in data.items()
                  if k in _CAMPOS_VALIDOS and v not in (None, '', 'null', 'N/A')}
        return campos, f'ok:{modelo}'

    except Exception as e:
        return {}, f'error:{type(e).__name__}: {str(e)[:120]}'


# ═══════════════════════════════════════════════════════════════════════════════
# DETECCIÓN DE PÁGINA POR CAMPO
# ═══════════════════════════════════════════════════════════════════════════════

def _detectar_paginas(campos: dict, paginas_texto: list[str]) -> dict:
    """
    Para cada campo extraído busca en qué página (1-based) aparece su valor.
    Solo busca valores con más de 2 caracteres para evitar falsos positivos.
    """
    resultado = {}
    for campo, valor in campos.items():
        val = str(valor).strip()
        if len(val) <= 2:
            continue
        val_coma = val.replace('.', ',')
        for i, texto_pag in enumerate(paginas_texto, start=1):
            if val in texto_pag or val_coma in texto_pag:
                resultado[campo] = i
                break
    return resultado


# ═══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

LIMITE_TABLAS_BYTES = 3 * 1024 * 1024   # pdfplumber solo en PDFs ≤ 3 MB


def extraer_todo(archivo) -> tuple[str, dict, dict, str]:
    """
    Devuelve (texto_crudo, campos_extraidos, paginas, gemini_status).
    - paginas: {campo: num_pagina}
    - gemini_status: 'ok:<modelo>' | 'sin_key' | 'error:<detalle>'
    """
    contenido = archivo.read()
    tam = len(contenido)

    # ── 1. Extracción de texto por página ────────────────────────────────────
    paginas_texto: list[str] = []
    texto = ''
    try:
        import fitz
        doc = fitz.open(stream=contenido, filetype='pdf')
        paginas_texto = [pag.get_text('text') or '' for pag in doc]
        doc.close()
        texto = '\n'.join(t for t in paginas_texto if t.strip())
    except Exception:
        try:
            import pdfplumber as _plumber
            with _plumber.open(io.BytesIO(contenido)) as pdf:
                paginas_texto = [pag.extract_text() or '' for pag in pdf.pages]
            texto = '\n'.join(t for t in paginas_texto if t.strip())
        except Exception as e:
            raise RuntimeError(f'No se pudo leer el PDF: {e}')

    if not texto:
        raise RuntimeError('El PDF no contiene texto legible.')

    # ── 2. Campos desde regex (texto libre) ───────────────────────────────────
    campos = campos_de_texto(texto)

    # ── 3. Tablas (solo PDFs ≤ 3 MB) ─────────────────────────────────────────
    if tam <= LIMITE_TABLAS_BYTES:
        try:
            tablas = extraer_tablas(contenido)
            for k, v in campos_de_tablas(tablas).items():
                if k not in campos:
                    campos[k] = v
        except Exception:
            pass

    # ── 4. Gemini (si hay API key, sobreescribe con mayor precisión) ──────────
    gemini_status = 'sin_key'
    try:
        gemini_campos, gemini_status = campos_de_gemini(texto)
        campos.update(gemini_campos)
    except Exception as e:
        gemini_status = f'error:{e}'

    # ── 5. Detectar página de cada campo ─────────────────────────────────────
    paginas = _detectar_paginas(campos, paginas_texto)

    return texto, campos, paginas, gemini_status


# Alias para compatibilidad con views.py anterior
def extraer_texto(archivo):
    contenido = archivo.read()
    try:
        return _texto_pymupdf(contenido)
    except Exception:
        return _texto_pdfplumber(io.BytesIO(contenido))


def extraer_campos(texto: str) -> dict:
    return campos_de_texto(texto)
