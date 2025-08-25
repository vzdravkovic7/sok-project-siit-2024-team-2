import json
from graph.api.models import Graph
from graph.api.services.plugin import DataSourcePlugin
from graph.api.services.graph_factory import GraphFactory

class JsonGraph(Graph):
    """Graph implementation specialized for JSON-based data.

    This subclass of `Graph` provides mechanisms to:
    - Store nodes and edges.
    - Ensure no duplicate edges are added.
    - Retrieve neighboring nodes for a given node.

    Attributes:
        _nodes (dict[str, Node]): Internal storage of nodes keyed by their ID.
        _edges (list[Edge]): List of edges in the graph.
        _edge_set (set[tuple]): Helper set to avoid duplicate edges.
    """

    def __init__(self):
        """Initializes an empty `JsonGraph` instance."""
        super().__init__()
        self._edge_set = set()

    def add_node(self, node):
        """Adds a node to the graph.

        Args:
            node (Node): The node instance to add.
        """
        self._nodes[node.node_id] = node

    def add_edge(self, edge):
        """Adds an edge to the graph, preventing duplicates.

        If the edge's destination node (`to_node`) is not None,
        duplicates are avoided using an internal edge set.
        Otherwise, the edge is added directly.

        Args:
            edge (Edge): The edge instance to add.
        """
        if edge.to_node is not None:
            edge_key = (edge.from_node.node_id, edge.to_node.node_id)
            if edge_key not in self._edge_set:
                self._edges.append(edge)
                self._edge_set.add(edge_key)
        else:
            self._edges.append(edge)

    def get_neighbors(self, node_id: str):
        """Retrieves all neighboring nodes for a given node ID.

        Args:
            node_id (str): The ID of the node whose neighbors should be returned.

        Returns:
            list[Node]: A list of neighboring nodes.
        """
        return [
            e.to_node
            for e in self._edges
            if e.from_node.node_id == node_id and e.to_node is not None
        ]

    @property
    def nodes(self):
        """Returns a list of all nodes in the graph.

        Returns:
            list[Node]: All nodes stored in the graph.
        """
        return list(self._nodes.values())

    @property
    def edges(self):
        """Returns a list of all edges in the graph.

        Returns:
            list[Edge]: All edges stored in the graph.
        """
        return self._edges

class JsonDatasource(DataSourcePlugin):
    """Data source plugin for loading graph data from JSON files.

    This plugin loads entities from a JSON file and converts them
    into a `JsonGraph` instance using `GraphFactory`.

    Example JSON structure:
        {
            "people": [
                {"id": "1", "name": "Alice", "references": ["2"]},
                {"id": "2", "name": "Bob"}
            ]
        }

    The plugin will automatically detect the first list of entities
    in the JSON file and use it to build the graph.
    """

    def name(self) -> str:
        """Returns the human-readable name of the plugin.

        Returns:
            str: Plugin name ("JSON Datasource").
        """
        return "JSON Datasource"

    def identifier(self) -> str:
        """Returns the unique identifier of the plugin.

        Returns:
            str: Plugin identifier ("datasource_json").
        """
        return "datasource_json"

    def load(self, **kwargs) -> JsonGraph:
        """Loads entities from a JSON file and builds a graph.

        Args:
            **kwargs: Must contain a `file_path` key with the path
                to the JSON file.

        Raises:
            ValueError: If `file_path` is missing or if no valid
                entity list is found in the JSON file.

        Returns:
            JsonGraph: A graph instance built from the JSON data.

        Example:
            >>> ds = JsonDatasource()
            >>> graph = ds.load(file_path="people.json")
            >>> len(graph.nodes)
            2
        """
        file_path = kwargs.get("file_path")

        if not file_path:
            raise ValueError("file_path must be provided in kwargs")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entities = None
        for k, v in data.items():
            if isinstance(v, list):
                entities = v
                break

        if not entities:
            raise ValueError("JSON file must contain at least one list of entities")

        return GraphFactory.from_entities(entities, JsonGraph)
