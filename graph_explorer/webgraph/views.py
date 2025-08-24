import os
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from graph.use_cases.plugin_recognition import PluginService
from graph.use_cases.graph_main_view import MainView
from .apps import datasource_group, visualizer_group

def _get_active_workspace(request):
    workspaces = request.session.get("workspaces", {})
    active = request.session.get("active_workspace")
    if not active or active not in workspaces:
        return None, workspaces
    return workspaces[active], workspaces

def index(request):
    plugin_service: PluginService = apps.get_app_config('webgraph').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]

    workspace, workspaces = _get_active_workspace(request)
    graph_view_header, graph_view_body = "", ""
    uploaded_file_name = None

    if workspace:
        datasource_id = workspace.get("datasource")
        visualizer_id = workspace.get("visualizer")
        selected_file = workspace.get("file")
        if selected_file:
            uploaded_file_name = os.path.basename(selected_file)
        if datasource_id and visualizer_id:
            graph_view = MainView(plugin_service)
            graph_view_header, graph_view_body = graph_view.render(
                datasource_id,
                visualizer_id,
                file_path=selected_file,
                request=request,
                workspace=workspace,
            )

    return render(request, 'index.html', {
        'title': 'Graph Explorer',
        'datasource_plugins': datasource_plugins,
        'visualizer_plugins': visualizer_plugins,
        'graph_view_header': graph_view_header,
        'graph_view_body': graph_view_body,
        'workspaces': workspaces,
        'active_workspace': request.session.get("active_workspace"),
        'active_datasource': workspace.get("datasource") if workspace else None,
        'active_visualizer': workspace.get("visualizer") if workspace else None,
        'uploaded_file_name': uploaded_file_name,
        'active_workspace_data': workspace,
    })

def add_workspace(request):
    name = request.GET.get("name", f"Workspace {len(request.session.get('workspaces', {})) + 1}")
    workspaces = request.session.get("workspaces", {})
    if name not in workspaces:
        workspaces[name] = {}
    request.session["workspaces"] = workspaces
    request.session["active_workspace"] = name
    request.session.modified = True
    return redirect("index")

def select_workspace(request, name):
    workspaces = request.session.get("workspaces", {})
    if name in workspaces:
        request.session["active_workspace"] = name
        request.session.modified = True
    return redirect("index")

def datasource_plugin(request, id):
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        workspace["datasource"] = id
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect('index')

def visualizer_plugin(request, id):
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        workspace["visualizer"] = id
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect('index')

def upload_file(request):
    workspace, workspaces = _get_active_workspace(request)
    if request.method == "POST":
        if "data_file" not in request.FILES:
            return HttpResponse("<script>alert('No file selected!'); window.location.href='/';</script>")
        uploaded_file = request.FILES["data_file"]
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb+") as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
        if workspace is not None:
            workspace["file"] = file_path
            request.session["workspaces"] = workspaces
            request.session.modified = True
        return redirect("index")
    return render(request, "upload.html")

def reset_graph(request):
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        workspace.pop("filters", None)
        workspace.pop("searches", None)
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect("index")

def remove_filter(request, index):
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        filters = workspace.get("filters") or []
        if 0 <= index < len(filters):
            filters.pop(index)
        workspace["filters"] = filters
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect("index")

def remove_search(request, index):
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        searches = workspace.get("searches") or []
        if 0 <= index < len(searches):
            searches.pop(index)
        workspace["searches"] = searches
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect("index")

def query_graph(request):
    workspace, workspaces = _get_active_workspace(request)
    if request.method == "POST" and workspace is not None:
        try:
            if request.POST.get("search"):
                searches = workspace.get("searches") or []
                searches = list(searches)
                searches.append(request.POST["search"])
                workspace["searches"] = searches
            if request.POST.get("filter1") and request.POST.get("operator") and request.POST.get("filter2"):
                filters = workspace.get("filters") or []
                filters = list(filters)
                filters.append({
                    "attr": request.POST["filter1"],
                    "op": request.POST["operator"],
                    "val": request.POST["filter2"]
                })
                workspace["filters"] = filters
            request.session["workspaces"] = workspaces
            request.session.modified = True
        except ValueError as e:
            return HttpResponse(f"<script>alert('{str(e)}'); window.location.href='/';</script>")
    return redirect("index")

def delete_workspace(request, name):
    workspaces = request.session.get("workspaces", {})
    active = request.session.get("active_workspace")
    if name in workspaces:
        del workspaces[name]
        if active == name:
            request.session["active_workspace"] = next(iter(workspaces), None)
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect("index")
