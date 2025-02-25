import os
import json
from jinja2 import Template
from .const import DATASOURCE_GROUP, VISUALIZER_GROUP
from .plugin_recognition import PluginService

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../../simple_visualizer/templates")
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)


class MainView(object):
    def __init__(self, plugin_service: PluginService):
        self.__plugin_service = plugin_service

    def render(self, datasource_id: str, visualizer_id: str, **kwargs) -> (str, str):
        """
        Uses the data source plugin to load a graph, then passes it to the visualizer plugin
        to generate the header and body HTML.

        :param datasource_id: ID of the data source plugin used to fetch data.
        :param visualizer_id: ID of the visualizer plugin used to render the graph.
        :param kwargs: Arguments for the data source plugin.
        :return: (header, body) HTML strings to be included in the page.
        """
        graph = None
        datasource_plugins = self.__plugin_service.plugins.get(DATASOURCE_GROUP, [])

        # Load the graph from the data source plugin
        for plugin in datasource_plugins:
            if plugin.identifier() == datasource_id:
                graph = plugin.load(**kwargs)
                break

        if not graph:
            return "", ""  # If no graph is found, return empty content

        visualizer_plugins = self.__plugin_service.plugins.get(VISUALIZER_GROUP, [])

        # Find the visualizer plugin
        visualizer = None
        for plugin in visualizer_plugins:
            if plugin.identifier() == visualizer_id:
                visualizer = plugin
                break

        if not visualizer:
            return "", ""  # If no matching visualizer is found, return empty content

        # Use the visualizer plugin to generate the HTML
        return visualizer.visualize(graph)
