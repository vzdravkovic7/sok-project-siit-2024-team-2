import os
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from graph.use_cases.plugin_recognition import PluginService
from graph.use_cases.graph_main_view import MainView
from .apps import datasource_group, visualizer_group

def index(request):
    plugin_service: PluginService = apps.get_app_config('webgraph').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]
    return render(request, 'index.html', {
        'title': 'Graph Explorer',
        'datasource_plugins': datasource_plugins,
        'visualizer_plugins': visualizer_plugins
    })


def datasource_plugin(request, id):
    request.session['selected_datasource_plugin'] = id
    return redirect('index')


def visualizer_plugin(request, id):
    request.session['selected_visualizer_plugin'] = id
    return redirect('index')


def graph_layout(request):
    selected_datasource_plugin = request.session.get('selected_datasource_plugin')
    selected_visualizer_plugin = request.session.get('selected_visualizer_plugin')
    selected_file = request.session.get("selected_json_file", None)

    plugin_service: PluginService = apps.get_app_config('webgraph').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]

    graph_view = MainView(plugin_service)

    header, body = graph_view.render(
        selected_datasource_plugin,
        selected_visualizer_plugin,
        file_name=selected_file,
        request=request,
    )

    return render(request, 'graph-simple-layout.html', {
        'title': 'Graph Layout',
        'datasource_plugins': datasource_plugins,
        'visualizer_plugins': visualizer_plugins,
        'graph_view_header': header,
        'graph_view_body': body
    })


def upload_json(request):
    if request.method == "POST":
        if "json_file" not in request.FILES:
            return HttpResponse(
                    "<script>alert('No JSON file selected!'); window.location.href='/layout/simple';</script>"
                )
        uploaded_file = request.FILES["json_file"]

        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, uploaded_file.name)

        with open(file_path, "wb+") as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        request.session["selected_json_file"] = file_path
        return redirect("graph_layout")

    return render(request, "upload.html")

def reset_graph(request):
    request.session.pop("filters", None)
    request.session.pop("searches", None)
    return redirect("graph_layout")

def remove_filter(request, index):
    filters = request.session.get("filters", [])
    if 0 <= index < len(filters):
        filters.pop(index)
        request.session["filters"] = filters
    return redirect("graph_layout")

def remove_search(request, index):
    searches = request.session.get("searches", [])
    if 0 <= index < len(searches):
        searches.pop(index)
        request.session["searches"] = searches
    return redirect("graph_layout")

def query_graph(request):
    if request.method == "POST":
        try:
            if request.POST.get("search"):
                searches = request.session.get("searches", [])
                searches.append(request.POST["search"])
                request.session["searches"] = searches

            if request.POST.get("filter1") and request.POST.get("operator") and request.POST.get("filter2"):
                filters = request.session.get("filters", [])
                filters.append({
                    "attr": request.POST["filter1"],
                    "op": request.POST["operator"],
                    "val": request.POST["filter2"]
                })
                request.session["filters"] = filters

        except ValueError as e:
            return HttpResponse(
                f"<script>alert('{str(e)}'); window.location.href='/layout/simple';</script>"
            )

    return redirect("graph_layout")
