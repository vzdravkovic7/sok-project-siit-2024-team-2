from abc import ABC
from typing import Union
from datetime import date

GraphValue = Union[int, str, float, date]

class Node(ABC):
    def __init__(self, node_id: str, value: GraphValue):
        self._node_id = node_id
        self._value = value

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def value(self) -> GraphValue:
        return self._value

    @value.setter
    def value(self, new_value: GraphValue):
        if isinstance(new_value, (int, str, float, date)):
            self._value = new_value
        else:
            raise TypeError("Invalid value type")

    def __str__(self):
        return f"Node({self.node_id}, {self.value})"