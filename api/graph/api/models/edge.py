from abc import ABC
from .node import Node

class Edge(ABC):
    """
    Abstract class representing an edge between two nodes in a graph.

    Attributes:
        _from_node (Node): The source node of the edge.
        _to_node (Node): The destination node of the edge.
        _weight (float): The weight of the edge, default is 1.0.
    """

    def __init__(self, from_node: Node, to_node: Node, weight: float = 1.0):
        """
        Initialize an edge with source and destination nodes and optional weight.

        Args:
            from_node (Node): The source node.
            to_node (Node): The destination node.
            weight (float, optional): The weight of the edge. Defaults to 1.0.
        """
        self._from_node = from_node
        self._to_node = to_node
        self._weight = weight

    @property
    def from_node(self) -> Node:
        """Return the source node of the edge."""
        return self._from_node

    @property
    def to_node(self) -> Node:
        """Return the destination node of the edge."""
        return self._to_node

    @property
    def weight(self) -> float:
        """Return the weight of the edge."""
        return self._weight

    @weight.setter
    def weight(self, value: float):
        """
        Set the weight of the edge.

        Args:
            value (float): The new weight.

        Raises:
            TypeError: If the value is not an int or float.
        """
        if isinstance(value, (int, float)):
            self._weight = float(value)
        else:
            raise TypeError("Weight must be a float or int")

    def __str__(self):
        """
        Return a string representation of the edge.

        Returns:
            str: Format 'Edge(from_node_id -> to_node_id, weight=value)'.
        """
        return f"Edge({self.from_node.node_id} -> {self.to_node.node_id}, weight={self.weight})"
