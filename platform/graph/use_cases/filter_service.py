from datetime import datetime
from graph.api.models import Graph, Node, Edge


class FilterService:
    @staticmethod
    def apply_filters(graph: Graph, filters: list[dict]) -> Graph:
        """
        Primeni listu filtera sukcesivno. 
        Filter je dict oblika: {"attr": "age", "op": ">", "val": "30"}
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
        """
        Pokušaj da parsiraš vrednost u broj ili datum, 
        ako ne uspe ostavi string.
        """
        if value is None:
            return None

        # pokušaj int
        try:
            return int(value)
        except ValueError:
            pass

        # pokušaj float
        try:
            return float(value)
        except ValueError:
            pass

        # pokušaj datetime (ISO ili dd.mm.yyyy)
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        # fallback string
        return str(value)

    @staticmethod
    def _compare(left, op: str, right) -> bool:
        """Uporedi dve vrednosti zavisno od operatora."""
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == ">": return left > right
        if op == ">=": return left >= right
        if op == "<": return left < right
        if op == "<=": return left <= right
        raise ValueError(f"Nepoznat operator: {op}")

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
                # ako tipovi nisu kompatibilni, preskoči
                continue

        # Dodaj samo grane između čuvanih čvorova
        for e in graph.edges:
            if e.from_node.node_id in keep and (e.to_node is None or e.to_node.node_id in keep):
                filtered.add_edge(e)

        return filtered
