from datetime import datetime
from graph.api.models import Graph

class FilterService:
    """Service class for applying attribute-based filters on graphs.

    This service allows filtering nodes in a graph by applying
    conditions on their attributes. Supported data types include
    integers, floats, dates, and strings. The result is a subgraph
    containing only nodes and edges that satisfy the filters.
    """

    @staticmethod
    def apply_filters(graph: Graph, filters: list[dict]) -> Graph:
        """Applies multiple filters to a graph.

        Each filter is a dictionary with the keys:
        - `"attr"`: The attribute name to filter by.
        - `"op"`: The comparison operator (`==`, `!=`, `>`, `>=`, `<`, `<=`).
        - `"val"`: The value to compare against.

        Args:
            graph (Graph): The graph to filter.
            filters (list[dict]): A list of filter definitions.

        Returns:
            Graph: A subgraph containing only nodes and edges that
            satisfy all provided filters.

        Example:
            >>> filters = [{"attr": "age", "op": ">", "val": "18"}]
            >>> result = FilterService.apply_filters(graph, filters)
            >>> len(result.nodes)
            3
        """
        if not filters:
            return graph

        subgraph = graph
        for f in filters:
            attr = f.get("attr")
            op = f.get("op")
            val = f.get("val")
            subgraph = FilterService._apply_filter(subgraph, attr, op, val)

        return subgraph

    @staticmethod
    def _parse_value(value: str):
        """Attempts to parse a string into int, float, datetime, or fallback string.

        Args:
            value (str): The input value.

        Returns:
            Union[int, float, datetime, str, None]: Parsed value or None.
        """
        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        for fmt in ("%Y-%m-%d", "%d.%m.%Y.", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        return str(value)

    @staticmethod
    def _compare(left, op: str, right) -> bool:
        """Compares two values using the given operator.

        Args:
            left: The left-hand operand.
            op (str): Comparison operator (`==`, `!=`, `>`, `>=`, `<`, `<=`).
            right: The right-hand operand.

        Returns:
            bool: Result of the comparison.

        Raises:
            ValueError: If the operator is not recognized.
        """
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == ">": return left > right
        if op == ">=": return left >= right
        if op == "<": return left < right
        if op == "<=": return left <= right
        raise ValueError(f"Unknown operator: {op}")

    @staticmethod
    def _apply_filter(graph: Graph, attr: str, op: str, val: str) -> Graph:
        """Applies a single filter to a graph.

        Args:
            graph (Graph): The input graph to filter.
            attr (str): The attribute name to check.
            op (str): The comparison operator.
            val (str): The value to compare against.

        Returns:
            Graph: A subgraph with only the nodes and edges that pass the filter.
        """
        filtered = type(graph)()
        keep = set()

        cmp_val = FilterService._parse_value(val)

        for node in graph.nodes:
            node_val = node.values.get(attr)
            if node_val is None:
                continue

            parsed_val = FilterService._parse_value(node_val)

            try:
                if FilterService._compare(parsed_val, op, cmp_val):
                    filtered.add_node(node)
                    keep.add(node.node_id)
            except Exception:
                continue

        for e in graph.edges:
            if e.from_node.node_id in keep and (e.to_node is None or e.to_node.node_id in keep):
                filtered.add_edge(e)

        return filtered
