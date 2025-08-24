from graph.api.models import Graph

class SearchService:
    @staticmethod
    def search(graph: Graph, queries: list[str]) -> Graph:
        if not queries:
            return graph

        queries = [str(q).lower() for q in queries if q]

        subgraph = type(graph)()
        matched_nodes = {}

        for node in graph.nodes:
            for value in node.values.items():
                value_str = str(value).lower()

                if any(q in value_str for q in queries):
                    subgraph.add_node(node)
                    matched_nodes[node.node_id] = node
                    break

        for edge in graph.edges:
            if (edge.from_node.node_id in matched_nodes and edge.to_node.node_id in matched_nodes):
                subgraph.add_edge(edge)

        return subgraph
