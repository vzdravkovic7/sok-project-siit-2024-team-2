import os
import json
import random
from jinja2 import Template
from graph.api.models import Graph, Node
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
        Returns the required header and body HTML content for rendering the graph visualization.
        Includes both data_json for standard views and tree_data_json for the tree view.
        """
        data_json = json.dumps(self.__generate_graph_data(graph), ensure_ascii=False)
        tree_data_json = json.dumps(self.__generate_tree_data(graph), ensure_ascii=False)

        # Load header template
        with open(os.path.join(TEMPLATES_DIR, "graph-visualizer-header.html"), "r", encoding="utf-8") as file:
            header_html = file.read()

        # Load body template
        with open(os.path.join(TEMPLATES_DIR, "graph-visualizer-body.html"), "r", encoding="utf-8") as file:
            body_template = file.read()

        # Render the template with both data sets
        body_html = Template(body_template).render(data_json=data_json, tree_data_json=tree_data_json)
        return header_html, body_html

    def __generate_graph_data(self, graph: Graph) -> dict:
        """
        Converts the graph into a structured format for visualization.
        """
        nodes = [{"id": node.node_id, "name": str(node.value), "x": float(node.x), "y": float(node.y)} for node in graph.nodes]
        edges = [
            {"from": edge.from_node.node_id, "to": edge.to_node.node_id, "weight": edge.weight}
            for edge in graph.edges if edge.to_node is not None
        ]

        return {
            "nodes": nodes,
            "edges": edges
        }

    def __generate_tree_data(self, graph: Graph) -> list[dict]:
        """
        Converts the graph into a forest of hierarchical trees without infinite recursion.
        Ensures that all nodes are included, even if they are isolated or in disconnected components.
        """

        if not graph.nodes:
            return []

        # Build adjacency list
        adjacency = {node.node_id: [] for node in graph.nodes}
        for edge in graph.edges:
            if edge.from_node and edge.to_node:
                adjacency[edge.from_node.node_id].append(edge.to_node)

        def build_tree(node: Node, visited: set) -> dict:
            """ Recursively build the tree structure from a given node. """
            if node.node_id in visited:
                return None

            visited.add(node.node_id)
            children = []

            for child_node in adjacency.get(node.node_id, []):
                if child_node.node_id not in visited:
                    child_tree = build_tree(child_node, visited)
                    if child_tree:
                        children.append(child_tree)

            return {
                "id": f"node_{node.node_id}",
                "name": str(node.value),
                "children": children
            }

        visited = set()
        forest = []

        # Build a tree for each connected component
        for node in graph.nodes:
            if node.node_id not in visited:
                tree = build_tree(node, visited)
                if tree:
                    forest.append(tree)

        # If no edges, isolated nodes should still appear as single-node trees
        for node in graph.nodes:
            if all(node.node_id != t["id"].replace("node_", "") for t in forest):
                forest.append({
                    "id": f"node_{node.node_id}",
                    "name": str(node.value),
                    "children": []
                })

        return forest
