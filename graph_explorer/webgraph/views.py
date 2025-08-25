import os
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from graph.use_cases.plugin_recognition import PluginService
from graph.use_cases.graph_main_view import MainView
from graph.use_cases.executor import GraphCLI
from .apps import datasource_group, visualizer_group

def _get_active_workspace(request):
    """
    Retrieve the currently active workspace from the session.

    Args:
        request: Django request object containing session data.

    Returns:
        tuple: (active_workspace, all_workspaces) where
            - active_workspace (dict or None): The currently active workspace configuration.
            - all_workspaces (dict): All workspaces stored in the session.
    """
    workspaces = request.session.get("workspaces", {})
    active = request.session.get("active_workspace")
    if not active or active not in workspaces:
        return None, workspaces
    return workspaces[active], workspaces

def index(request):
    """
    Render the main application page with available plugins and active workspace.

    Args:
        request: Django request object.

    Returns:
        HttpResponse: Rendered index.html with context data.
    """
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
    """
    Add a new workspace to the session and set it as active.

    Args:
        request: Django request object.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
    name = request.GET.get("name", f"Workspace {len(request.session.get('workspaces', {})) + 1}")
    workspaces = request.session.get("workspaces", {})
    if name not in workspaces:
        workspaces[name] = {}
    request.session["workspaces"] = workspaces
    request.session["active_workspace"] = name
    request.session.modified = True
    return redirect("index")

def select_workspace(request, name):
    """
    Select an existing workspace as active.

    Args:
        request: Django request object.
        name (str): Name of the workspace to activate.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
    workspaces = request.session.get("workspaces", {})
    if name in workspaces:
        request.session["active_workspace"] = name
        request.session.modified = True
    return redirect("index")

def datasource_plugin(request, id):
    """
    Set the datasource plugin for the active workspace.

    Args:
        request: Django request object.
        id (str): Identifier of the datasource plugin.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        workspace["datasource"] = id
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect('index')

def visualizer_plugin(request, id):
    """
    Set the visualizer plugin for the active workspace.

    Args:
        request: Django request object.
        id (str): Identifier of the visualizer plugin.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        workspace["visualizer"] = id
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect('index')

def upload_file(request):
    """
    Handle file upload and associate the uploaded file with the active workspace.

    Args:
        request: Django request object.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to index on success, or returns
        error alert if no file selected.
    """
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
    """
    Reset filters and searches for the active workspace.

    Args:
        request: Django request object.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        workspace.pop("filters", None)
        workspace.pop("searches", None)
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect("index")

def remove_filter(request, index):
    """
    Remove a filter by index from the active workspace.

    Args:
        request: Django request object.
        index (int): Index of the filter to remove.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
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
    """
    Remove a search query by index from the active workspace.

    Args:
        request: Django request object.
        index (int): Index of the search to remove.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
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
    """
    Handle queries (searches and filters) submitted by the user.

    Args:
        request: Django request object.

    Returns:
        HttpResponseRedirect: Redirect to index view, possibly with updated searches/filters.
    """
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
    """
    Delete a workspace from the session.

    Args:
        request: Django request object.
        name (str): Name of the workspace to delete.

    Returns:
        HttpResponseRedirect: Redirect to index view.
    """
    workspaces = request.session.get("workspaces", {})
    active = request.session.get("active_workspace")
    if name in workspaces:
        del workspaces[name]
        if active == name:
            request.session["active_workspace"] = next(iter(workspaces), None)
        request.session["workspaces"] = workspaces
        request.session.modified = True
    return redirect("index")

from django.shortcuts import redirect

def terminal_command(request):
    """
    Handle a terminal command submitted via POST request.

    Supports:
        - 'cls' to clear the terminal history.
        - 'filter <conditions>' to add filter conditions to the active workspace.
        - 'search <keyword>' to add search keywords to the active workspace.
        - Any other command is stored in the CLI commands list of the workspace.

    Args:
        request (HttpRequest): Django HTTP request containing the command in POST data.

    Returns:
        HttpResponseRedirect: Redirects to the 'index' page after processing.
    """
    if request.method != "POST":
        return redirect("index")

    command = request.POST.get("command", "").strip()
    if not command:
        return redirect("index")

    if command.lower() == "cls":
        return clear_terminal(request)

    workspace, workspaces = _get_active_workspace(request)
    if workspace is not None:
        tokens = command.split(maxsplit=1)
        cmd_type = tokens[0].lower()
        rest = tokens[1].strip() if len(tokens) > 1 else ""

        if cmd_type == "filter" and rest:
            filters = workspace.get("filters", [])
            for cond in rest.split("&&"):
                cond = cond.strip()
                for op in ["==", "!=", ">=", "<=", ">", "<"]:
                    if op in cond:
                        parts = cond.split(op, 1)
                        if len(parts) == 2:
                            attr, val = parts
                            filters.append({
                                "attr": attr.strip(),
                                "op": op,
                                "val": val.strip()
                            })
                        break
            workspace["filters"] = filters

        elif cmd_type == "search" and rest:
            searches = workspace.get("searches", [])
            keyword = rest.split()[0]
            searches.append(keyword)
            workspace["searches"] = searches

        else:
            cli_commands = workspace.get("cli_commands", [])
            cli_commands.append(command)
            workspace["cli_commands"] = cli_commands

        request.session["workspaces"] = workspaces
        request.session.modified = True

    history = request.session.get("terminal_history", [])
    history.append({"text": f"> {command}", "type": "command"})
    request.session["terminal_history"] = history

    return redirect("index")


def clear_terminal(request):
    """
    Clear the terminal history stored in the session.

    Args:
        request (HttpRequest): Django HTTP request.

    Returns:
        HttpResponseRedirect: Redirects to the 'index' page after clearing.
    """
    if "terminal_history" in request.session:
        request.session["terminal_history"] = []
        request.session.modified = True
    return redirect("index")
