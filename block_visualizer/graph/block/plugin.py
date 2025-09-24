import os
import json
from jinja2 import Template
from graph.api.models import Graph, Node
from graph.api.services.plugin import VisualizerPlugin

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../templates")
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)


class BlockVisualizer(VisualizerPlugin):
    def name(self) -> str:
        return "Block View"

    def identifier(self) -> str:
        return "block_visualizer"

    def visualize(self, graph: Graph) -> (str, str):
        """
        Returns the required header and body HTML content for rendering the graph visualization.
        Includes both data_json for standard views and tree_data_json for the tree view.
        """
        data_json = json.dumps(self.__generate_graph_data(graph), ensure_ascii=False)
        tree_data_json = json.dumps(self.__generate_tree_data(graph), ensure_ascii=False)

        with open(os.path.join(TEMPLATES_DIR, "graph-visualizer-header.html"), "r", encoding="utf-8") as file:
            header_html = file.read()

        with open(os.path.join(TEMPLATES_DIR, "graph-visualizer-body.html"), "r", encoding="utf-8") as file:
            body_template = file.read()

        body_html = Template(body_template).render(data_json=data_json, tree_data_json=tree_data_json)
        return header_html, body_html

    
