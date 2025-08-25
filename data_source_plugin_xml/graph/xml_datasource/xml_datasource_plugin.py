import xml.etree.ElementTree as ET
from typing import Dict, Optional

from graph.api.models import Graph, Node, Edge
from graph.api.services.plugin import DataSourcePlugin


class XMLNode(Node):
    """Node for XML plugin holding id and key-value attributes."""

    def __init__(self, node_id: str, values: dict, x: float = None, y: float = None):
        """Initialize XMLNode with optional coordinates."""
        
        super().__init__(node_id, values, x, y)


class XMLEdge(Edge):
    """Edge for XML plugin representing connection between two nodes."""
    pass


class XMLGraph(Graph):
    """Simple Graph implementation for XML plugin."""

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""

        self._nodes[node.node_id] = node

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""

        self._edges.append(edge)

    def get_neighbors(self, node_id: str):
        """Return a list of neighbor nodes for a given node id."""

        return [e.to_node for e in self._edges if e.from_node.node_id == node_id]

    @property
    def nodes(self):
        """Return all nodes in the graph."""

        return list(self._nodes.values())

    @property
    def edges(self):
        """Return all edges in the graph."""

        return self._edges


class XMLDataSourcePlugin(DataSourcePlugin):
    """Data source plugin for loading graphs from XML files."""

    def name(self) -> str:
        """Return the human-readable name of the plugin."""

        return "XML Data Source Plugin"

    def identifier(self) -> str:
        """Return the unique identifier of the plugin."""

        return "xml_datasource"

    def _create_node(self, elem) -> Optional[XMLNode]:
        """Create an XMLNode if the element has an 'id' attribute, otherwise None."""

        node_id = elem.attrib.get("id")
        if not node_id:
            return None

        values = {
            child.tag: child.text.strip()
            for child in elem
            if not child.attrib and child.text and child.text.strip()
        }

        values["id"] = node_id

        return XMLNode(node_id, values)

    def _create_edge(self, parent_id: Optional[str], elem, id_to_node: Dict[str, XMLNode]) -> Optional[XMLEdge]:
        """Create an XMLEdge if element has 'reference' attribute and both nodes exist."""

        if "reference" in elem.attrib and parent_id:
            ref_id = elem.attrib["reference"]
            if parent_id in id_to_node and ref_id in id_to_node:
                return XMLEdge(id_to_node[parent_id], id_to_node[ref_id])
        return None

    def _collect_nodes(self, elem, graph: XMLGraph, id_to_node: Dict[str, XMLNode]) -> None:
        """First pass: collect all nodes."""

        node = self._create_node(elem)
        if node:
            graph.add_node(node)
            id_to_node[node.node_id] = node

        for child in elem:
            self._collect_nodes(child, graph, id_to_node)

    def _collect_edges(
        self,
        elem,
        graph: XMLGraph,
        id_to_node: Dict[str, XMLNode],
        current_parent_id: Optional[str] = None,
    ) -> None:
        """Second pass: collect all edges."""

        node_id = elem.attrib.get("id", current_parent_id)

        edge = self._create_edge(node_id, elem, id_to_node)
        if edge:
            graph.add_edge(edge)

        for child in elem:
            self._collect_edges(child, graph, id_to_node, node_id)

    def load(self, **kwargs) -> Graph:
        """Load an XML file and convert it into a Graph."""

        file_path = kwargs.get("file_path")
        if not file_path:
            raise ValueError("file_path must be provided in kwargs")

        tree = ET.parse(file_path)
        root = tree.getroot()

        graph = XMLGraph()
        id_to_node: Dict[str, XMLNode] = {}

        self._collect_nodes(root, graph, id_to_node)
        self._collect_edges(root, graph, id_to_node)

        return graph
