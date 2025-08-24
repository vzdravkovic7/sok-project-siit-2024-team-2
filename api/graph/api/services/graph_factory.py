from graph.api.models import Node, Edge, Graph

class GraphFactory:
    """Factory class responsible for building Graph objects from raw entity data."""

    @staticmethod
    def from_entities(entities: list[dict], graph_class: type[Graph]) -> Graph:
        """
        Generic method to build a graph from a list of entity dictionaries.
        Expects each entity to have 'id' and optional 'references'.
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
