from graph.api.models import Node, Edge, Graph

class GraphFactory:
    """Factory class responsible for constructing Graph objects from raw entity data.

    This class provides utilities to convert raw dictionaries representing entities
    into a `Graph` object composed of `Node` and `Edge` instances. It expects that
    each entity includes a unique identifier (`id`) and may contain references to
    other entities, which are translated into directed edges.
    """

    @staticmethod
    def from_entities(entities: list[dict], graph_class: type[Graph]) -> Graph:
        """Builds a graph from a list of entity dictionaries.

        Each dictionary must contain an `"id"` key and may optionally contain
        a `"references"` key, which should be a list of other entity IDs that
        this entity points to. The method will create `Node` objects for each
        entity and `Edge` objects for each reference.

        Args:
            entities (list[dict]): A list of entity data, where each entity is
                represented as a dictionary with an `"id"` field and optionally
                a `"references"` field.
            graph_class (type[Graph]): The class used to instantiate the resulting
                graph. Must be a subclass of `Graph`.

        Returns:
            Graph: A graph instance containing nodes and edges derived from the
            provided entities.

        Example:
            >>> entities = [
            ...     {"id": "1", "name": "Alice", "references": ["2"]},
            ...     {"id": "2", "name": "Bob"}
            ... ]
            >>> graph = GraphFactory.from_entities(entities, Graph)
            >>> len(graph.nodes)
            2
            >>> len(graph.edges)
            1
        """
        graph = graph_class()
        node_map = {}

        for entity in entities:
            node_id = str(entity.get("id"))
            if not node_id:
                continue

            values = {k: v for k, v in entity.items() if k != "references"}
            node = Node(node_id=node_id, values=values)
            graph.add_node(node)
            node_map[node_id] = node

        for entity in entities:
            src = node_map.get(str(entity.get("id")))
            if not src:
                continue

            refs = entity.get("references", [])
            if isinstance(refs, list):
                for ref_id in refs:
                    dst = node_map.get(str(ref_id))
                    if dst:
                        graph.add_edge(Edge(from_node=src, to_node=dst))

        return graph
