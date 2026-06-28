import json
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from pacientes.models import Paciente
from .catalogo import SECCIONES, CATALOGO
from . import stats as S


def estadisticas_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if request.user.is_superuser or request.user.groups.filter(name='estadisticas').exists():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapped


@estadisticas_required
def dashboard(request):
    total = Paciente.objects.count()
    return render(request, 'estadisticas/dashboard.html', {
        'secciones': SECCIONES,
        'total_pacientes': total,
    })


@estadisticas_required
@require_POST
def analizar(request):
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'Petición inválida'}, status=400)

    campos = body.get('variables', [])
    filtro = body.get('filtro', 'todos')

    if not campos:
        return JsonResponse({'error': 'Selecciona al menos una variable'}, status=400)

    # Validar que todos los campos existen en el catálogo
    for c in campos:
        if c not in CATALOGO:
            return JsonResponse({'error': f'Variable desconocida: {c}'}, status=400)

    # Construir queryset
    qs = Paciente.objects.all()
    if filtro == 'completado':
        qs = qs.filter(estado='completado')
    elif filtro == 'pendiente':
        qs = qs.filter(estado='pendiente')

    n_total = qs.count()
    if n_total == 0:
        return JsonResponse({'error': 'No hay pacientes con ese filtro'}, status=200)

    # ── Resumen agrupado por tipo de diagnóstico ──────────────────────────────
    if len(campos) == 1 and CATALOGO[campos[0]].get('tipo') == 'resumen_tipos':
        meta = CATALOGO[campos[0]]
        all_diag = list(qs.values_list('diagnostico', flat=True))
        tipos = meta['tipos']
        counts = [
            sum(1 for v in all_diag if t in (v or '').split(','))
            for t, _ in tipos
        ]
        labels = [lbl for _, lbl in tipos]
        pcts = [round(c / n_total * 100, 1) if n_total else 0 for c in counts]
        return JsonResponse({
            'modo': 'resumen_tipos',
            'label': meta['label'],
            'n_total_bd': n_total,
            'labels': labels,
            'counts': counts,
            'pcts': pcts,
        })

    def _valores(campo):
        meta = CATALOGO[campo]
        db_campo = meta.get('source_campo', campo)
        raw = list(qs.values_list(db_campo, flat=True))

        if meta.get('multivalue_extract'):
            target = meta['multivalue_extract']
            return ['si' if target in (v or '').split(',') else 'no' for v in raw]

        if meta.get('multivalue'):
            choices = meta.get('choices', [])
            label_map = dict(choices)
            orden = [val for val, _ in choices]
            result = []
            for v in raw:
                if v:
                    vals = {x.strip() for x in v.split(',') if x.strip()}
                    partes = [label_map[k] for k in orden if k in vals]
                    result.append(' + '.join(partes))
                else:
                    result.append('')
            return result

        return raw

    # ── Univariado ────────────────────────────────────────────────────────────
    if len(campos) == 1:
        campo = campos[0]
        meta = CATALOGO[campo]
        vals = _valores(campo)

        if meta['tipo'] == 'numerico':
            resultado = S.describe_numeric(vals)
        else:
            choices = None if meta.get('no_choices_filter') else meta.get('choices')
            resultado = S.describe_categorical(vals, choices=choices)

        resultado['label'] = meta['label']
        resultado['seccion'] = meta['seccion']
        resultado['n_total_bd'] = n_total
        resultado['modo'] = 'univariado'
        return JsonResponse(resultado)

    # ── Bivariado ─────────────────────────────────────────────────────────────
    if len(campos) == 2:
        c1, c2 = campos
        m1, m2 = CATALOGO[c1], CATALOGO[c2]
        v1 = _valores(c1)
        v2 = _valores(c2)
        t1, t2 = m1['tipo'], m2['tipo']

        if t1 == 'numerico' and t2 == 'numerico':
            resultado = S.bivar_num_num(v1, v2)
        elif t1 == 'numerico' and t2 == 'categorico':
            resultado = S.bivar_num_cat(v1, v2, choices_cat=m2.get('choices'))
        elif t1 == 'categorico' and t2 == 'numerico':
            resultado = S.bivar_num_cat(v2, v1, choices_cat=m1.get('choices'))
            resultado['label_num'], resultado['label_cat'] = m2['label'], m1['label']
        elif t1 == 'categorico' and t2 == 'categorico':
            resultado = S.bivar_cat_cat(v1, v2, m1.get('choices'), m2.get('choices'))
        else:
            resultado = {'error': 'Combinación no soportada'}

        resultado.setdefault('label_x', m1['label'])
        resultado.setdefault('label_y', m2['label'])
        resultado.setdefault('label_num', m1['label'] if t1 == 'numerico' else m2['label'])
        resultado.setdefault('label_cat', m2['label'] if t2 == 'categorico' else m1['label'])
        resultado['modo'] = 'bivariado'
        resultado['n_total_bd'] = n_total
        return JsonResponse(resultado)

    # ── Multivariado: hasta 6 vars, univariados individuales ──────────────────
    resultados = []
    for campo in campos[:6]:
        meta = CATALOGO[campo]
        vals = _valores(campo)
        if meta['tipo'] == 'numerico':
            r = S.describe_numeric(vals)
        else:
            choices = None if meta.get('no_choices_filter') else meta.get('choices')
            r = S.describe_categorical(vals, choices=choices)
        r['label'] = meta['label']
        r['campo'] = campo
        resultados.append(r)

    return JsonResponse({'modo': 'multivariado', 'resultados': resultados, 'n_total_bd': n_total})
