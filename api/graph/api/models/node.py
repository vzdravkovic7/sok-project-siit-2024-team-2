from abc import ABC
from typing import Union
from datetime import date
import random

GraphValue = Union[int, str, float, date]

class Node(ABC):
    def __init__(self, node_id: str, values: dict[str, GraphValue] = None, x: float = None, y: float = None):
        self._node_id = node_id
        self._values: dict[str, GraphValue] = values if values is not None else {}
        self._x = x if x is not None else random.uniform(0, 1000)
        self._y = y if y is not None else random.uniform(0, 1000)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def values(self) -> dict[str, GraphValue]:
        return self._values

    def set_value(self, key: str, value: GraphValue):
        if isinstance(value, (int, str, float, date)):
            self._values[key] = value
        else:
            raise TypeError("Value must be int, str, float or date")

    def get_value(self, key: str) -> GraphValue:
        return self._values.get(key)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, new_x: float):
        if isinstance(new_x, (int, float)):
            self._x = float(new_x)
        else:
            raise TypeError("x coordinate must be a number")

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new_y: float):
        if isinstance(new_y, (int, float)):
            self._y = float(new_y)
        else:
            raise TypeError("y coordinate must be a number")

    def __str__(self):
        return f"Node({self.node_id}, values={self._values}, x={self.x}, y={self.y})"