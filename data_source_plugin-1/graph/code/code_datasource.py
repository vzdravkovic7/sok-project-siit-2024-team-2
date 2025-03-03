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
        nodes = []

        # Pre-generate positions for consistency
        positions = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(200)]

        for i, (x, y) in enumerate(positions):
            node = Node(node_id=str(i), value=random.randint(10, 1000), x=x, y=y)
            graph.add_node(node)
            nodes.append(node)

        # Generate 400 edges, ensuring they reference actual node objects
        edges = []
        for _ in range(400):
            from_node, to_node = random.sample(nodes, 2)
            weight = round(random.uniform(1.0, 10.0), 2)
            edges.append(Edge(from_node=from_node, to_node=to_node, weight=weight))

        for edge in edges:
            graph.add_edge(edge)

        return graph
