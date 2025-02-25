import os
import json
from jinja2 import Template
from graph.api.models import Graph
from graph.api.services.plugin import VisualizerPlugin

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../templates")
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)


class SimpleVisualizer(VisualizerPlugin):
    def name(self) -> str:
        return "Simple View"

    def identifier(self) -> str:
        return "simple_visualizer"

    def visualize(self, graph: Graph) -> (str, str):
        """
        Returns the required header and body HTML content for rendering a simple graph visualization.
        """
        graph_data = self.__generate_graph_data(graph)
        data_json = json.dumps(graph_data, ensure_ascii=False)

        # Load header template
        with open(os.path.join(TEMPLATES_DIR, "graph-visualizer-header.html"), "r", encoding="utf-8") as file:
            header_html = file.read()

        # Load body template
        with open(os.path.join(TEMPLATES_DIR, "graph-visualizer-body.html"), "r", encoding="utf-8") as file:
            body_template = file.read()

        body_html = Template(body_template).render(data_json=data_json)
        return header_html, body_html

    def __generate_graph_data(self, graph: Graph) -> dict:
        """
        Converts the graph into a structured format for visualization.
        """
        nodes = [{"id": node.node_id, "name": str(node.value)} for node in graph.nodes]
        edges = [{"from": edge.from_node.node_id, "to": edge.to_node.node_id, "weight": edge.weight} for edge in graph.edges]

        return {
            "nodes": nodes,
            "edges": edges
        }
