import csv
import io
import json
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from functools import wraps
from .models import ValorReferencia, HORMONA_CHOICES
from .forms import ValorReferenciaForm
from . import excel_importer

HORMONA_VALORES = {label.lower(): val for val, label in HORMONA_CHOICES}
HORMONA_VALORES.update({val.lower(): val for val, label in HORMONA_CHOICES})

CSV_COLUMNAS = [
    'hormona', 'version', 'grupo_clinico', 'tipo_muestra',
    'unidad', 'ref_min', 'ref_max',
    'unidad2', 'ref_min2', 'ref_max2',
    'intervalo_min', 'intervalo_max', 'observaciones',
]


def role_required(*grupos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.groups.filter(name__in=grupos).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapped
    return decorator


def superuser_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapped


@login_required
def lista(request):
    hormona_sel = request.GET.get('hormona', '')
    qs = ValorReferencia.objects.all()
    if hormona_sel:
        qs = qs.filter(hormona=hormona_sel)

    # Agrupar por hormona para la vista
    grupos = {}
    for vr in qs:
        grupos.setdefault(vr.get_hormona_display(), []).append(vr)

    return render(request, 'referencias/lista.html', {
        'grupos':       grupos,
        'hormonas':     HORMONA_CHOICES,
        'hormona_sel':  hormona_sel,
    })


@role_required('administrador', 'medico')
def crear(request):
    hormona_inicial = request.GET.get('hormona', '')
    initial = {'hormona': hormona_inicial} if hormona_inicial else {}
    form = ValorReferenciaForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Valor de referencia guardado.')
        return redirect('referencias:lista')
    return render(request, 'referencias/form.html', {'form': form, 'titulo': 'Nuevo valor de referencia'})


@role_required('administrador', 'medico')
def editar(request, pk):
    vr = get_object_or_404(ValorReferencia, pk=pk)
    form = ValorReferenciaForm(request.POST or None, instance=vr)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Valor de referencia actualizado.')
        return redirect('referencias:lista')
    return render(request, 'referencias/form.html', {
        'form': form,
        'titulo': f'Editar — {vr.get_hormona_display()} {vr.version}',
        'object': vr,
    })


@login_required
def api_hormona(request, hormona):
    def _f(v):
        return float(v) if isinstance(v, Decimal) else v

    registros = ValorReferencia.objects.filter(hormona=hormona).order_by('version', 'grupo_clinico')
    data = []
    for vr in registros:
        label = vr.version
        if vr.grupo_clinico:
            label += f' · {vr.grupo_clinico}'
        data.append({
            'label':   label,
            'ref_min': _f(vr.ref_min),
            'ref_max': _f(vr.ref_max),
            'unidad':  vr.unidad,
        })
    return JsonResponse({'grupos': data})


@superuser_required
def importar_excel(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        modo    = request.POST.get('modo', 'crear')
        if not archivo:
            messages.error(request, 'Seleccione un archivo Excel.')
            return redirect('referencias:importar_excel')
        if not archivo.name.lower().endswith(('.xlsx', '.xls')):
            messages.error(request, 'Solo se aceptan archivos .xlsx o .xls.')
            return redirect('referencias:importar_excel')
        try:
            resultado = excel_importer.importar_excel(archivo, modo=modo)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('referencias:importar_excel')

        resumen = (
            f"Importación completada: "
            f"{resultado['creados']} creados, "
            f"{resultado['actualizados']} actualizados, "
            f"{resultado['omitidos']} omitidos."
        )
        if resultado['errores']:
            resumen += f" {len(resultado['errores'])} errores."
        messages.success(request, resumen)
        return render(request, 'referencias/importar_excel.html', {
            'resultado': resultado,
        })

    return render(request, 'referencias/importar_excel.html', {})


@role_required('administrador')
def exportar_csv(request):
    fecha = datetime.now().strftime('%Y%m%d_%H%M')
    resp = HttpResponse(content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = f'attachment; filename="referencias_{fecha}.csv"'
    resp.write('﻿')
    writer = csv.writer(resp)
    writer.writerow(CSV_COLUMNAS)
    for vr in ValorReferencia.objects.all():
        writer.writerow([
            vr.hormona, vr.version, vr.grupo_clinico, vr.tipo_muestra,
            vr.unidad, vr.ref_min or '', vr.ref_max or '',
            vr.unidad2, vr.ref_min2 or '', vr.ref_max2 or '',
            vr.intervalo_min or '', vr.intervalo_max or '', vr.observaciones,
        ])
    return resp


@superuser_required
def importar_csv(request):
    if request.method == 'GET':
        return render(request, 'referencias/importar_csv.html')

    archivo = request.FILES.get('csv_file')
    if not archivo:
        messages.error(request, 'No se seleccionó ningún archivo.')
        return render(request, 'referencias/importar_csv.html')
    if not archivo.name.lower().endswith('.csv'):
        messages.error(request, 'El archivo debe tener extensión .csv')
        return render(request, 'referencias/importar_csv.html')

    try:
        contenido = archivo.read().decode('utf-8-sig')
    except UnicodeDecodeError:
        archivo.seek(0)
        contenido = archivo.read().decode('latin-1')

    modo = request.POST.get('modo', 'crear')
    if modo == 'reemplazar':
        ValorReferencia.objects.all().delete()

    def _dec(val):
        val = str(val).strip().replace(',', '.')
        if not val:
            return None
        try:
            return Decimal(val)
        except InvalidOperation:
            return None

    reader = csv.DictReader(io.StringIO(contenido))
    creados = actualizados = omitidos = 0
    errores = []

    for i, row in enumerate(reader, start=2):
        hormona = row.get('hormona', '').strip().lower()
        hormona = HORMONA_VALORES.get(hormona, '')
        version = row.get('version', '').strip()
        if not hormona or not version:
            errores.append((i, 'hormona y version son obligatorios'))
            continue

        grupo_clinico = row.get('grupo_clinico', '').strip()
        defaults = {
            'tipo_muestra':  row.get('tipo_muestra', '').strip(),
            'unidad':        row.get('unidad', '').strip(),
            'ref_min':       _dec(row.get('ref_min', '')),
            'ref_max':       _dec(row.get('ref_max', '')),
            'unidad2':       row.get('unidad2', '').strip(),
            'ref_min2':      _dec(row.get('ref_min2', '')),
            'ref_max2':      _dec(row.get('ref_max2', '')),
            'intervalo_min': _dec(row.get('intervalo_min', '')),
            'intervalo_max': _dec(row.get('intervalo_max', '')),
            'observaciones': row.get('observaciones', '').strip(),
        }
        try:
            if modo == 'crear':
                _, created = ValorReferencia.objects.get_or_create(
                    hormona=hormona, version=version, grupo_clinico=grupo_clinico,
                    defaults=defaults,
                )
                if created:
                    creados += 1
                else:
                    omitidos += 1
            else:
                _, created = ValorReferencia.objects.update_or_create(
                    hormona=hormona, version=version, grupo_clinico=grupo_clinico,
                    defaults=defaults,
                )
                if created:
                    creados += 1
                else:
                    actualizados += 1
        except Exception as e:
            errores.append((i, str(e)))

    resultado = {'creados': creados, 'actualizados': actualizados,
                 'omitidos': omitidos, 'errores': errores}
    return render(request, 'referencias/importar_csv.html', {'resultado': resultado})


@role_required('administrador')
def eliminar(request, pk):
    vr = get_object_or_404(ValorReferencia, pk=pk)
    if request.method == 'POST':
        vr.delete()
        messages.success(request, 'Valor de referencia eliminado.')
        return redirect('referencias:lista')
    return render(request, 'referencias/confirmar_eliminar.html', {'vr': vr})
