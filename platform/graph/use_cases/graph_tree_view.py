import os
import json
from jinja2 import Template
from typing import List

from graph.code.code_datasource import SimpleGraph
from .const import DATASOURCE_GROUP
from .plugin_recognition import PluginService

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../templates")
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)

class TreeView(object):
    def __init__(self, plugin_service: PluginService):
        self.__plugin_service = plugin_service

    def render(self, plugin_id: str, **kwargs) -> (str, str):
        """
        Returns the required header and body HTML content that needs to be included in the page
        to provide a tree view layout.

        :param plugin_id: ID of the data source plugin used to fetch data.
        :param kwargs: Arguments for the data source plugin.
        :return: (header, body) HTML strings to be included in the page.
        """
        graph = None
        plugins = self.__plugin_service.plugins.get(DATASOURCE_GROUP, [])

        for plugin in plugins:
            if plugin.identifier() == plugin_id:
                graph = plugin.load(**kwargs)  # Load the graph

        if not graph:
            return "", ""  # If no graph is found, return empty content

        tree_data = self.__generate_tree_data(graph)
        data_json = json.dumps(tree_data, ensure_ascii=False)

        with open(os.path.join(TEMPLATES_DIR, "graph-tree-layout-header.html"), "r", encoding="utf-8") as file:
            header_html = file.read()

        with open(os.path.join(TEMPLATES_DIR, "graph-tree-layout-body.html"), "r", encoding="utf-8") as file:
            body_template = file.read()

        body_html = Template(body_template).render(data_json=data_json)
        return header_html, body_html

    def __generate_tree_data(self, graph: SimpleGraph) -> dict:
        """
        Constructs a hierarchical structure for nodes, connecting them based on the edges.

        :param graph: Graph instance containing nodes and edges.
        :return: JSON-like dictionary representing the tree structure.
        """

        # Create the structure for tree nodes based on edges
        children = []
        for edge in graph.edges:
            from_node = edge.from_node
            to_node = edge.to_node
            children.append({
                'id': f'node_{from_node.node_id}',
                'name': str(from_node.value),
                'children': [
                    {
                        'id': f'node_{to_node.node_id}',
                        'name': str(to_node.value),
                    }
                ]
            })

        return {
            "id": "Graph",
            "name": "Graph",
            "children": children
        }
