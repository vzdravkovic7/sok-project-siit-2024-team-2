from django.apps import apps
from django.shortcuts import render, redirect

from graph.use_cases.plugin_recognition import PluginService

from graph.use_cases.graph_main_view import MainView
from .apps import datasource_group, visualizer_group


def index(request):
    plugin_service: PluginService = apps.get_app_config('webgraph').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]
    return render(request, 'index.html', {'title': 'Graph Explorer', 'datasource_plugins': datasource_plugins, 'visualizer_plugins': visualizer_plugins})


def datasource_plugin(request, id):
    request.session['selected_datasource_plugin'] = id
    return redirect('index')


def visualizer_plugin(request, id):
    request.session['selected_visualizer_plugin'] = id
    return redirect('index')


def graph_layout(request):
    selected_datasource_plugin = request.session['selected_datasource_plugin']
    selected_visualizer_plugin = request.session['selected_visualizer_plugin']
    plugin_service: PluginService = apps.get_app_config('webgraph').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]

    graph_view = MainView(plugin_service)
    header, body = graph_view.render(selected_datasource_plugin, selected_visualizer_plugin)

    return render(request, 'graph-simple-layout.html',
                  {'title': 'Graph Layout',
                   'datasource_plugins': datasource_plugins,
                   'visualizer_plugins': visualizer_plugins,
                   'graph_view_header': header,
                   'graph_view_body': body})
