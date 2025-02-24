from typing import List

from graph.api.models import Node, Edge, Graph
from graph.api.services.plugin import DataSourcePlugin

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

    def load(self) -> SimpleGraph:
        # Creating nodes with different values
        nodeA = Node(node_id="A", value=10)
        nodeB = Node(node_id="B", value=20)
        nodeC = Node(node_id="C", value=30)
        nodeD = Node(node_id="D", value=50)
        nodeE = Node(node_id="E", value=70)
        nodeF = Node(node_id="F", value=90)
        nodeG = Node(node_id="G", value=100)
        nodeH = Node(node_id="H", value=120)

        # Creating edges
        edges = [
            Edge(from_node=nodeA, to_node=nodeB, weight=5.0),
            Edge(from_node=nodeB, to_node=nodeC, weight=3.5),
            Edge(from_node=nodeC, to_node=nodeD, weight=2.0),
            Edge(from_node=nodeD, to_node=nodeE, weight=1.5),
            Edge(from_node=nodeE, to_node=nodeF, weight=4.0),
            Edge(from_node=nodeF, to_node=nodeG, weight=6.0),
            Edge(from_node=nodeG, to_node=nodeH, weight=3.0),
            Edge(from_node=nodeB, to_node=nodeE, weight=2.5),
            Edge(from_node=nodeD, to_node=nodeG, weight=7.0)
        ]

        # Creating a graph and adding nodes and edges
        graph = SimpleGraph()
        for node in [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG, nodeH]:
            graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

        return graph
