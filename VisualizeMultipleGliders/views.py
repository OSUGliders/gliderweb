from django.shortcuts import render
import plotly.express as px
from VisualizeMultipleGliders.models import Glider, Glider_Research_Data
from VisualizeMultipleGliders.slocum_documents import (
    get_slocum_documents_context,
)
from VisualizeMultipleGliders.seaglider_documents import (
    get_seaglider_documents_context,
)
from django.utils import timezone
import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import io
import csv
import urllib.request
import urllib.parse


def glider_map_view(request):
    return render(request, 'gliderdata/glider_map.html')
def remove_nan(obj):
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: remove_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [remove_nan(x) for x in obj]
    return obj


def plot_glider_data(request):
    variables_units={'temperature': '°C', 'salinity': 'PSU', 'oxygen': 'ml/l', 'depth':'m'}
    colorscales_range={'temperature': [6,12]}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gliderID=data.get("glider_id")
            track = data.get("track", [])
            x_axis = data.get("x_axis")
            y_axis = data.get("y_axis")
            color=data.get("color")
            if not track:
                return JsonResponse({'plot_html': "<p>No data provided.</p>"})
            df = pd.DataFrame(track)
            start_time = str(df['startOfCoverage'].iloc[0])
            end_time = str(df['endOfCoverage'].iloc[0])
            id = gliderID.split("-")[0]
            title = f"{id}_{start_time.replace(':','').replace('-','').replace('T','')}-{end_time.replace(':','').replace('-','').replace('T','')}"
            y_unit = variables_units.get(y_axis)
            color_unit=variables_units.get(color)
            scale=colorscales_range.get(color)
            df['precise_time'] = pd.to_datetime(df['time'],format="ISO8601", utc=True)
            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,  
                color=color,  
                color_continuous_scale='thermal',
                template='plotly_white',
                range_color=scale,
                title=title,
                hover_data=[x_axis,y_axis,color]
            )
            fig.update_layout(
            coloraxis_colorbar=dict(
                title=f"{color} ({color_unit})"
            ),
            xaxis_title=f"{x_axis}",
            yaxis_title=f"{y_axis}, ({y_unit})",
            title_x=0.5,
            title_font=dict(size=16)
            )
            fig.update_layout(width=1000)
            fig.update_yaxes(autorange='reversed')
            return JsonResponse({'plot_html': fig.to_html(full_html=False)})
        except Exception as e:
            return JsonResponse({'plot_html': f"<p>Error: {str(e)}</p>"})
def glider_data_to_display(request):
    glider_param = request.GET.get('glider')
    qs = Glider_Research_Data.objects
    if glider_param:
        qs = qs.filter(glider__glider_id=glider_param)
    data = list(
        qs.values('glider__glider_id','glider__startOfCoverage',
            'glider__endOfCoverage','precise_time', 'precise_lat', 'precise_lon', 'depth','temperature', 'oxygen','salinity')
    )
    cleaned_data = remove_nan(data)
    return JsonResponse(cleaned_data, safe=False)


def home_page(request):
    return render(request, "gliderdata/home_page.html")

def people(request):
    return render(request, "gliderdata/people.html")

def projects(request):
    return render(request, "gliderdata/projects.html")


def deployments(request):
    now = timezone.now()
    gliders = Glider.objects.all().order_by('-startOfCoverage')
    active = []
    historical = []

    def find_erddap_dataset(glider_id):
        base_tokens = []
        if not glider_id:
            return None
        base_tokens.append(glider_id)
        if '_' in glider_id:
            base_tokens.append(glider_id.split('_')[0])
        if '-' in glider_id:
            base_tokens.append(glider_id.split('-')[0])
        digits = ''.join([c for c in glider_id if c.isdigit()])
        if digits:
            base_tokens.append(digits)

        seen = set()
        for tok in base_tokens:
            if not tok or tok in seen:
                continue
            seen.add(tok)
            try:
                q = urllib.parse.quote(tok)
                url = f"https://gliders.ioos.us/erddap/search/index.csv?searchFor={q}&itemsPerPage=10"
                req = urllib.request.Request(url, headers={'User-Agent':'gliderweb/1.0'})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    data = resp.read().decode('utf-8', errors='replace')
                f = io.StringIO(data)
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row and row[0]:
                        return row[0]
            except Exception:
                continue
        return None
    for g in gliders:
        entry = {
            'id': g.glider_id,
            'start': g.startOfCoverage,
            'end': g.endOfCoverage,
        }
        found = find_erddap_dataset(g.glider_id)
        if found:
            entry['erddap'] = f"https://gliders.ioos.us/erddap/tabledap/{found}.html"
        else:
            entry['erddap'] = f"https://gliders.ioos.us/erddap/tabledap/{g.glider_id}.html"
        if g.endOfCoverage is None or (g.endOfCoverage and g.endOfCoverage > now):
            active.append(entry)
        else:
            historical.append(entry)
    return render(request, 'gliderdata/deployments.html', {'active_deployments': active, 'historical_deployments': historical})


def documentation(request):
    slocum_ctx = get_slocum_documents_context()
    seaglider_ctx = get_seaglider_documents_context()
    masterdata_url = 'https://gliderfs.coas.oregonstate.edu/gliderweb/masterdata/'

    context = {
        'slocum_training_manuals': slocum_ctx.get('training_manuals', []),
        'slocum_technical_references': slocum_ctx.get('technical_references', []),
        'seaglider_operations': seaglider_ctx.get('operations_and_guides', []),
        'seaglider_technical': seaglider_ctx.get('technical_documentation', []),
        'masterdata_url': masterdata_url,
    }
    return render(request, 'gliderdata/documentation.html', context)

def statistics(request):
    return render(request, "gliderdata/statistics.html")

def data_products(request):
    return render(request, "gliderdata/data_products.html")

def publications(request):
    return render(request, "gliderdata/publications.html")