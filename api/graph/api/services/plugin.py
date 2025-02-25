from typing import Any, List
from abc import ABC, abstractmethod

from graph.api.models import Graph, Node


class Plugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """
        Retrieves the name of the plugin.

        :return: The name of the plugin.
        :rtype: str
        """
        pass

    @abstractmethod
    def identifier(self) -> str:
        """
        Retrieves a unique identifier for the plugin.

        :return: The unique identifier of the plugin.
        :rtype: str
        """
        pass

class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading graph data from a specific data source.
    """
    @abstractmethod
    def load(self, **kwargs) -> Graph:
        """
        Loads data from the data source and returns a `Graph` object with both nodes and edges.

        :param kwargs: Arbitrary keyword arguments for customization or filtering of the data loading process.
        :type kwargs: dict
        :return: A `Graph` object containing both `Node` and `Edge` objects.
        :rtype: Graph
        """
        pass

class VisualizerPlugin(ABC):
    """
    An abstraction representing a plugin for graph visualization.
    """

    @abstractmethod
    def name(self) -> str:
        """
        Retrieves the name of the simple plugin.

        :return: The name of the simple plugin.
        :rtype: str
        """
        pass

    @abstractmethod
    def identifier(self) -> str:
        """
        Retrieves a unique identifier for the simple plugin.

        :return: The unique identifier of the simple plugin.
        :rtype: str
        """
        pass

    @abstractmethod
    def visualize(self, graph: Graph) -> Any:
        """
        Processes a `Graph` object and returns a visualization representation.

        :param graph: The graph to visualize.
        :type graph: Graph
        :return: A visualization representation.
        :rtype: Any
        """
        pass
