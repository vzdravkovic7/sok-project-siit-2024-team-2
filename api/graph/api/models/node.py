from abc import ABC
from typing import Union
from datetime import date
import random

GraphValue = Union[int, str, float, date]

class Node(ABC):
    """
    Abstract class representing a graph node.

    Attributes:
        _node_id (str): Unique identifier of the node.
        _values (dict[str, GraphValue]): Key-value properties of the node.
        _x (float): X-coordinate for visualization or layout purposes.
        _y (float): Y-coordinate for visualization or layout purposes.
    """

    def __init__(self, node_id: str, values: dict[str, GraphValue] = None, x: float = None, y: float = None):
        """
        Initialize a node with an ID, optional values, and optional coordinates.

        Args:
            node_id (str): Unique identifier of the node.
            values (dict[str, GraphValue], optional): Node properties as key-value pairs.
            x (float, optional): X-coordinate. Randomly assigned if not provided.
            y (float, optional): Y-coordinate. Randomly assigned if not provided.
        """
        self._node_id = node_id
        self._values: dict[str, GraphValue] = values if values is not None else {}
        self._x = x if x is not None else random.uniform(0, 1000)
        self._y = y if y is not None else random.uniform(0, 1000)

    @property
    def node_id(self) -> str:
        """Return the unique identifier of the node."""
        return self._node_id

    @property
    def values(self) -> dict[str, GraphValue]:
        """Return all key-value properties of the node."""
        return self._values

    def set_value(self, key: str, value: GraphValue):
        """
        Set a property value for the node.

        Args:
            key (str): The property name.
            value (GraphValue): The value to set (int, str, float, or date).

        Raises:
            TypeError: If value is not int, str, float, or date.
        """
        if isinstance(value, (int, str, float, date)):
            self._values[key] = value
        else:
            raise TypeError("Value must be int, str, float or date")

    def get_value(self, key: str) -> GraphValue:
        """
        Get the value of a property by key.

        Args:
            key (str): The property name.

        Returns:
            GraphValue: The value of the property, or None if not set.
        """
        return self._values.get(key)

    @property
    def x(self) -> float:
        """Return the X-coordinate of the node."""
        return self._x

    @x.setter
    def x(self, new_x: float):
        """
        Set the X-coordinate of the node.

        Args:
            new_x (float): New X-coordinate.

        Raises:
            TypeError: If new_x is not a number.
        """
        if isinstance(new_x, (int, float)):
            self._x = float(new_x)
        else:
            raise TypeError("x coordinate must be a number")

    @property
    def y(self) -> float:
        """Return the Y-coordinate of the node."""
        return self._y

    @y.setter
    def y(self, new_y: float):
        """
        Set the Y-coordinate of the node.

        Args:
            new_y (float): New Y-coordinate.

        Raises:
            TypeError: If new_y is not a number.
        """
        if isinstance(new_y, (int, float)):
            self._y = float(new_y)
        else:
            raise TypeError("y coordinate must be a number")

    def __str__(self):
        """
        Return a string representation of the node.

        Returns:
            str: Node ID, values, and coordinates.
        """
        return f"Node({self.node_id}, values={self._values}, x={self.x}, y={self.y})"
