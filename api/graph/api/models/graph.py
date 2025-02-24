from abc import ABC, abstractmethod
from typing import List, Dict
from .node import Node
from .edge import Edge

class Graph(ABC):
    def __init__(self):
        self._nodes: Dict[str, Node] = {}
        self._edges: List[Edge] = []

    @abstractmethod
    def add_node(self, node: Node):
        pass

    @abstractmethod
    def add_edge(self, edge: Edge):
        pass

    @abstractmethod
    def get_neighbors(self, node_id: str) -> List[Node]:
        pass

    def __str__(self):
        return f"Graph with {len(self._nodes)} nodes and {len(self._edges)} edges"