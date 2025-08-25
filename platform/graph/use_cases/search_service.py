from graph.api.models import Graph

class SearchService:
    """Service class providing search functionality on graphs.

    This class exposes a static method to filter nodes and edges
    from a graph based on query strings. It produces a subgraph
    containing only the matching nodes and the edges between them.
    """

    @staticmethod
    def search(graph: Graph, queries: list[str]) -> Graph:
        """Performs a search on a graph based on a list of query strings.

        The method filters nodes whose values contain any of the
        provided query strings (case-insensitive). A new subgraph
        is returned, containing only the matching nodes and the
        edges that connect them.

        Args:
            graph (Graph): The graph to search within.
            queries (list[str]): A list of search query strings. If empty,
                the original graph is returned.

        Returns:
            Graph: A subgraph containing nodes and edges that match
            the given queries.

        Example:
            >>> from graph.api.models import Graph, Node, Edge
            >>> g = Graph()
            >>> g.add_node(Node("1", {"name": "Alice"}))
            >>> g.add_node(Node("2", {"name": "Bob"}))
            >>> g.add_edge(Edge(g.nodes[0], g.nodes[1]))
            >>> result = SearchService.search(g, ["alice"])
            >>> len(result.nodes)
            1
            >>> len(result.edges)
            0
        """
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
