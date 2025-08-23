from abc import ABC
from .node import Node

class Edge(ABC):
    def __init__(self, from_node: Node, to_node: Node = None, weight: float = 1.0, value=None, label: str = None):
        self._from_node = from_node
        self._to_node = to_node
        self._weight = weight
        self._value = value
        self._label = label

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

    @property
    def value(self):
        return self._value

    @property
    def label(self):
        return self._label

    def __str__(self):
        if self._to_node is not None:
            return f"Edge({self.from_node.node_id} -[{self.label or ''}]-> {self.to_node.node_id}, weight={self.weight})"
        else:
            return f"Edge({self.from_node.node_id} -[{self.label or ''}={self.value}])"
