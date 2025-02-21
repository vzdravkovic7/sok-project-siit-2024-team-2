from typing import List

from shop.api.models import Node, Edge, Graph
from shop.api.services.plugin import DataSourcePlugin

class SimpleGraph(Graph):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_neighbors(self, node):
        return [e.to_node for e in self.edges if e.from_node == node]


class CodeDatasource(DataSourcePlugin):
    def name(self) -> str:
        return "Graph Code Datasource"

    def identifier(self) -> str:
        return "datasource_code"

    def load(self) -> List[Node]:
        # Creating nodes
        node1 = Node(node_id="A", value=10)
        node2 = Node(node_id="B", value=20)
        node3 = Node(node_id="C", value=30)

        # Creating edges
        edge1 = Edge(from_node=node1, to_node=node2, weight=5.0)
        edge2 = Edge(from_node=node2, to_node=node3, weight=3.5)

        # Creating a graph and adding nodes and edges
        graph = SimpleGraph()
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        graph.add_edge(edge1)
        graph.add_edge(edge2)

        return [node1, node2, node3]  # Returning nodes (modify if needed)
