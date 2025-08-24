import os

from .const import DATASOURCE_GROUP, VISUALIZER_GROUP
from graph.use_cases.search_service import SearchService
from graph.use_cases.filter_service import FilterService
from .plugin_recognition import PluginService

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../../simple_visualizer/templates")
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)

class MainView(object):
    def __init__(self, plugin_service: PluginService):
        self.__plugin_service = plugin_service

    def render(self, datasource_id: str, visualizer_id: str, **kwargs) -> (str, str):
        if not datasource_id or not visualizer_id:
            return "", ""
        
        request = kwargs.get("request")
        if request and not request.session.get("searches") and not request.session.get("filters") and "reset" in request.GET:
            return "", ""

        datasource_plugins = self.__plugin_service.plugins.get(DATASOURCE_GROUP, [])
        graph = None

        for plugin in datasource_plugins:
            if plugin.identifier() == datasource_id:
                try:
                    clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}
                    request = kwargs.get("request")
                    print("REQUEST:", clean_kwargs)
                    graph = plugin.load(**clean_kwargs)
                    if request:
                        query = request.session.get("searches")
                        if query:
                            graph = SearchService.search(graph, query)

                        filters = request.session.get("filters")
                        if filters:
                            graph = FilterService.apply_filters(graph, filters)
                            
                except Exception as e:
                    print("Datasource plugin error:", e)
                    return "<h3>Error loading graph</h3>", ""
                break

        if not graph:
            return "<h3>No graph data available</h3>", ""

        visualizer_plugins = self.__plugin_service.plugins.get(VISUALIZER_GROUP, [])
        visualizer = next((p for p in visualizer_plugins if p.identifier() == visualizer_id), None)

        if not visualizer:
            return "<h3>No visualizer available</h3>", ""

        return visualizer.visualize(graph)
