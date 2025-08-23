import os
import json
from typing import Optional
from graph.api.models import Node, Edge, Graph
from graph.api.services.plugin import DataSourcePlugin

class JsonGraph(Graph):
    def __init__(self):
        super().__init__()
        self._edge_set = set()

    def add_node(self, node: Node):
        self._nodes[node.node_id] = node

    def add_edge(self, edge: Edge):
        if edge.to_node is not None:
            edge_key = (edge.from_node.node_id, edge.to_node.node_id, edge.label)
            if edge_key not in self._edge_set:
                self._edges.append(edge)
                self._edge_set.add(edge_key)
        else:
            self._edges.append(edge)

    def get_neighbors(self, node_id: str):
        return [e.to_node for e in self._edges if e.from_node.node_id == node_id and e.to_node is not None]

    @property
    def nodes(self):
        return list(self._nodes.values())

    @property
    def edges(self):
        return self._edges

class JsonDatasource(DataSourcePlugin):
    def name(self) -> str: return "JSON Datasource"
    def identifier(self) -> str: return "datasource_json"

    def load(
        self,
        file_name: Optional[str] = None,
        folder_path: str = "",
        searches: list = None,
        filters: list = None,
        **kwargs
    ) -> JsonGraph:
        if not file_name:
            raise ValueError("JSON Datasource requires a file_name argument")

        graph = JsonGraph()

        file_path = os.path.join(folder_path, file_name) if folder_path else file_name
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        person_map = {}
        for person in data.get("people", []):
            node = Node(node_id=person['id'], value=json.dumps(person))
            graph.add_node(node)
            person_map[person['id']] = node

        for person in data.get("people", []):
            src = person_map[person['id']]
            for key, val in person.items():
                if key == "id":
                    continue
                elif key == "friends":
                    for fid in val:
                        dst = person_map.get(fid)
                        if dst:
                            graph.add_edge(Edge(from_node=src, to_node=dst, label="friend"))
                else:
                    graph.add_edge(Edge(from_node=src, value=val, label=key))

        if searches:
            for query in searches:
                graph = self._apply_search(graph, query)

        if filters:
            for f in filters:
                graph = self._apply_filter(graph, f["attr"], f["op"], f["val"])

        return graph

    def _apply_search(self, graph: JsonGraph, query: str) -> JsonGraph:
        q = (query or "").strip().lower()
        filtered = JsonGraph()
        keep = set()

        for node in graph.nodes:
            bag = [str(node.node_id), str(node.value)]
            for e in graph.edges:
                if e.from_node == node:
                    bag.append(str(e.label))
                    if e.value is not None:
                        bag.append(str(e.value))

            if any(q in s.lower() for s in bag):
                filtered.add_node(node)
                keep.add(node.node_id)

        for e in graph.edges:
            if e.from_node.node_id in keep and (e.to_node is None or e.to_node.node_id in keep):
                filtered.add_edge(e)

        return filtered

    def _apply_filter(self, graph: JsonGraph, attr: str, op: str, val: str) -> JsonGraph:
        filtered = JsonGraph()
        keep = set()

        for node in graph.nodes:
            include = False
            for e in graph.edges:
                if e.from_node == node and e.label == attr:
                    node_val = e.value
                    try:
                        cmp_val = float(val)
                        node_val_num = float(node_val)
                        if op == "==": include = node_val_num == cmp_val
                        elif op == "!=": include = node_val_num != cmp_val
                        elif op == ">": include = node_val_num > cmp_val
                        elif op == ">=": include = node_val_num >= cmp_val
                        elif op == "<": include = node_val_num < cmp_val
                        elif op == "<=": include = node_val_num <= cmp_val
                    except Exception:
                        try:
                            s_cmp = str(val).lower()
                            s_node = str(node_val).lower()
                            if op == "==": include = s_node == s_cmp
                            elif op == "!=": include = s_node != s_cmp
                            else:
                                raise ValueError(f"Operator '{op}' nije podržan za string vrednosti.")
                        except Exception:
                            raise ValueError(f"Nevalidan tip za filter: {attr} {op} {val}")

            if include:
                filtered.add_node(node)
                keep.add(node.node_id)

        for e in graph.edges:
            if e.from_node.node_id in keep and (e.to_node is None or e.to_node.node_id in keep):
                filtered.add_edge(e)

        return filtered
