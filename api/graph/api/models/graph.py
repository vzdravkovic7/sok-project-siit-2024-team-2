from abc import ABC, abstractmethod
from typing import List, Dict
from .node import Node
from .edge import Edge

class Graph(ABC):
    """
    Abstract base class representing a graph structure with nodes and edges.

    Attributes:
        _nodes (Dict[str, Node]): A dictionary mapping node IDs to Node objects.
        _edges (List[Edge]): A list of Edge objects in the graph.
    """

    def __init__(self):
        """
        Initialize an empty graph with no nodes and no edges.
        """
        self._nodes: Dict[str, Node] = {}
        self._edges: List[Edge] = []

    @abstractmethod
    def add_node(self, node: Node):
        """
        Add a node to the graph.

        Args:
            node (Node): The node to add.
        """
        pass

    @abstractmethod
    def add_edge(self, edge: Edge):
        """
        Add an edge to the graph.

        Args:
            edge (Edge): The edge to add.
        """
        pass

    @abstractmethod
    def get_neighbors(self, node_id: str) -> List[Node]:
        """
        Get all neighboring nodes connected to the given node.

        Args:
            node_id (str): The ID of the node to find neighbors for.

        Returns:
            List[Node]: A list of neighboring Node objects.
        """
        pass

    def __str__(self):
        """
        Return a string representation of the graph.

        Returns:
            str: Description of the graph including number of nodes and edges.
        """
        return f"Graph with {len(self._nodes)} nodes and {len(self._edges)} edges"
