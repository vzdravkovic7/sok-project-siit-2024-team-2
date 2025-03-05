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
        edges = [{"from": edge.from_node.node_id, "to": edge.to_node.node_id, "weight": edge.weight} for edge in graph.edges]

        return {
            "nodes": nodes,
            "edges": edges
        }

    def __generate_tree_data(self, graph: Graph) -> dict:
        """
        Converts the graph into a hierarchical tree format without infinite recursion.
        Ensures that all nodes are included, even if they are not directly connected.
        """

        if not graph.nodes:
            return {}  # No nodes in the graph

        # Randomly select a starting node
        start_node = random.choice(graph.nodes)

        def build_tree(node: Node, visited: set):
            """
            Recursively build the tree structure from a given node.
            Uses the same visited set throughout recursion to prevent cycles efficiently.
            """
            if node.node_id in visited:
                return None  # Skip nodes already visited (prevents infinite loops)

            visited.add(node.node_id)

            children = []
            for edge in graph.edges:
                if edge.from_node.node_id == node.node_id and edge.to_node.node_id not in visited:
                    child_tree = build_tree(edge.to_node, visited)
                    if child_tree:  # Only add valid children
                        children.append(child_tree)

            return {
                "id": f"node_{node.node_id}",
                "name": str(node.value),
                "children": children
            }

        # Use a single visited set to avoid slow deep copies
        tree_data = build_tree(start_node, set())

        if not tree_data:
            # If no tree data was created (i.e., no children were found), create a base tree
            tree_data = {
                "id": f"node_{start_node.node_id}",
                "name": str(start_node.value),
                "children": []
            }

        # Add any unvisited nodes to the tree as children of the starting node
        visited_nodes = {start_node.node_id}
        for edge in graph.edges:
            visited_nodes.add(edge.from_node.node_id)
            visited_nodes.add(edge.to_node.node_id)

        for node in graph.nodes:
            if node.node_id not in visited_nodes:
                tree_data["children"].append({
                    "id": f"node_{node.node_id}",
                    "name": str(node.value),
                    "children": []
                })

        return tree_data
