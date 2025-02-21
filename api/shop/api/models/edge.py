from abc import ABC
from .node import Node

class Edge(ABC):
    def __init__(self, from_node: Node, to_node: Node, weight: float = 1.0):
        self._from_node = from_node
        self._to_node = to_node
        self._weight = weight

    @property
    def from_node(self) -> Node:
        return self._from_node

    @property
    def to_node(self) -> Node:
        return self._to_node

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float):
        if isinstance(value, (int, float)):
            self._weight = float(value)
        else:
            raise TypeError("Weight must be a float or int")

    def __str__(self):
        return f"Edge({self.from_node.node_id} -> {self.to_node.node_id}, weight={self.weight})"