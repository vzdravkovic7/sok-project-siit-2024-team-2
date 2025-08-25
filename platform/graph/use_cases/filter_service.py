from datetime import datetime
from graph.api.models import Graph

class FilterService:
    @staticmethod
    def apply_filters(graph: Graph, filters: list[dict]) -> Graph:
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
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == ">": return left > right
        if op == ">=": return left >= right
        if op == "<": return left < right
        if op == "<=": return left <= right
        raise ValueError(f"Unknown operator: {op}")

    @staticmethod
    def _apply_filter(graph: Graph, attr: str, op: str, val: str) -> Graph:
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
