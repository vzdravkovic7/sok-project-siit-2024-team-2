from abc import ABC, abstractmethod
from graph.api.models import Graph, Node, Edge
from typing import Dict


class Command(ABC):
    @abstractmethod
    def execute(self, graph: Graph):
        pass


class CreateNodeCommand(Command):
    def __init__(self, node_id, properties: Dict[str, str]):
        self.node_id = node_id
        self.properties = properties

    def execute(self, graph: Graph):
        if not self.node_id or self.node_id in graph._nodes:
            return
        node = Node(self.node_id, self.properties)
        graph.add_node(node)


class EditNodeCommand(Command):
    def __init__(self, node_id, properties: Dict[str, str]):
        self.node_id = node_id
        self.properties = properties or {}

    def execute(self, graph: Graph):
        node = graph._nodes.get(self.node_id)
        if not node:
            return
        for k, v in self.properties.items():
            node.set_value(k, v)


class DeleteNodeCommand(Command):
    def __init__(self, node_id):
        self.node_id = node_id

    def execute(self, graph: Graph):
        node = graph._nodes.get(self.node_id)
        if not node:
            return
        # Ako čvor ima bilo koju ivicu, ne briši
        if any(e.from_node.node_id == self.node_id or e.to_node.node_id == self.node_id for e in graph._edges):
            return
        del graph._nodes[self.node_id]


class CreateEdgeCommand(Command):
    def __init__(self, from_id, to_id):
        self.from_id = from_id
        self.to_id = to_id

    def execute(self, graph: Graph):
        from_node = graph._nodes.get(self.from_id)
        to_node = graph._nodes.get(self.to_id)
        if not from_node or not to_node:
            return
        if any(e.from_node.node_id == self.from_id and e.to_node.node_id == self.to_id for e in graph._edges):
            return
        graph.add_edge(Edge(from_node, to_node))


class DeleteEdgeCommand(Command):
    def __init__(self, from_id, to_id):
        self.from_id = from_id
        self.to_id = to_id

    def execute(self, graph: Graph):
        edge = next((e for e in graph._edges if e.from_node.node_id == self.from_id and e.to_node.node_id == self.to_id), None)
        if edge:
            graph._edges.remove(edge)


class ClearGraphCommand(Command):
    def execute(self, graph: Graph):
        graph._nodes.clear()
        graph._edges.clear()

