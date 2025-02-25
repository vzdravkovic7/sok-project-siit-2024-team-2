from typing import List
import random
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
        graph = SimpleGraph()

        # Generate 200 nodes with random values between 10 and 1000
        nodes = [Node(node_id=str(i), value=random.randint(10, 1000)) for i in range(200)]

        # Add nodes to the graph
        for node in nodes:
            graph.add_node(node)

        # Generate 400 random edges
        edges = []
        for _ in range(400):
            from_node, to_node = random.sample(nodes, 2)  # Pick two distinct nodes
            weight = round(random.uniform(1.0, 10.0), 2)  # Random weight between 1.0 and 10.0
            edges.append(Edge(from_node=from_node, to_node=to_node, weight=weight))

        # Add edges to the graph
        for edge in edges:
            graph.add_edge(edge)

        return graph
