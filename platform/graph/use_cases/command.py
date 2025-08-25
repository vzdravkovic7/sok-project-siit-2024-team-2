from abc import ABC, abstractmethod
from graph.api.models import Graph, Node, Edge
from typing import Dict


class Command(ABC):
    """
    Abstract base class for all graph commands.
    Each command should implement the execute method.
    """
    @abstractmethod
    def execute(self, graph: Graph):
        """
        Execute the command on the given graph.

        Args:
            graph (Graph): The graph on which the command will be executed.
        """
        pass


class CreateNodeCommand(Command):
    """
    Command to create a new node in the graph.
    """
    def __init__(self, node_id, properties: Dict[str, str]):
        """
        Initialize the command with a node ID and its properties.

        Args:
            node_id (str): The unique identifier of the node.
            properties (Dict[str, str]): Key-value properties of the node.
        """
        self.node_id = node_id
        self.properties = properties

    def execute(self, graph: Graph):
        """
        Execute the node creation. If the node ID already exists, do nothing.

        Args:
            graph (Graph): The graph where the node will be added.
        """
        if not self.node_id or self.node_id in graph._nodes:
            return
        node = Node(self.node_id, self.properties)
        graph.add_node(node)


class EditNodeCommand(Command):
    """
    Command to edit properties of an existing node.
    """
    def __init__(self, node_id, properties: Dict[str, str]):
        """
        Initialize the command with the node ID and properties to update.

        Args:
            node_id (str): The unique identifier of the node.
            properties (Dict[str, str]): Properties to update on the node.
        """
        self.node_id = node_id
        self.properties = properties or {}

    def execute(self, graph: Graph):
        """
        Update the node properties. If the node does not exist, do nothing.

        Args:
            graph (Graph): The graph containing the node to edit.
        """
        node = graph._nodes.get(self.node_id)
        if not node:
            return
        for k, v in self.properties.items():
            node.set_value(k, v)


class DeleteNodeCommand(Command):
    """
    Command to delete a node from the graph.
    """
    def __init__(self, node_id):
        """
        Initialize the command with the node ID to delete.

        Args:
            node_id (str): The unique identifier of the node.
        """
        self.node_id = node_id

    def execute(self, graph: Graph):
        """
        Delete the node if it exists and has no connected edges.

        Args:
            graph (Graph): The graph from which the node will be deleted.
        """
        node = graph._nodes.get(self.node_id)
        if not node:
            return
        if any(e.from_node.node_id == self.node_id or e.to_node.node_id == self.node_id for e in graph._edges):
            return
        del graph._nodes[self.node_id]


class CreateEdgeCommand(Command):
    """
    Command to create an edge between two nodes.
    """
    def __init__(self, from_id, to_id):
        """
        Initialize the command with source and target node IDs.

        Args:
            from_id (str): Source node ID.
            to_id (str): Target node ID.
        """
        self.from_id = from_id
        self.to_id = to_id

    def execute(self, graph: Graph):
        """
        Create an edge between the specified nodes if it doesn't already exist.

        Args:
            graph (Graph): The graph where the edge will be added.
        """
        from_node = graph._nodes.get(self.from_id)
        to_node = graph._nodes.get(self.to_id)
        if not from_node or not to_node:
            return
        if any(e.from_node.node_id == self.from_id and e.to_node.node_id == self.to_id for e in graph._edges):
            return
        graph.add_edge(Edge(from_node, to_node))


class DeleteEdgeCommand(Command):
    """
    Command to delete an edge between two nodes.
    """
    def __init__(self, from_id, to_id):
        """
        Initialize the command with source and target node IDs.

        Args:
            from_id (str): Source node ID.
            to_id (str): Target node ID.
        """
        self.from_id = from_id
        self.to_id = to_id

    def execute(self, graph: Graph):
        """
        Delete the edge between the specified nodes if it exists.

        Args:
            graph (Graph): The graph from which the edge will be deleted.
        """
        edge = next((e for e in graph._edges if e.from_node.node_id == self.from_id and e.to_node.node_id == self.to_id), None)
        if edge:
            graph._edges.remove(edge)


class ClearGraphCommand(Command):
    """
    Command to clear all nodes and edges from the graph.
    """
    def execute(self, graph: Graph):
        """
        Remove all nodes and edges from the graph.

        Args:
            graph (Graph): The graph to clear.
        """
        graph._nodes.clear()
        graph._edges.clear()
