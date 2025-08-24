import os
import json
from typing import Optional
from graph.api.models import Graph
from graph.api.services.plugin import DataSourcePlugin
from graph.api.services.graph_factory import GraphFactory


class JsonGraph(Graph):
    def __init__(self):
        super().__init__()
        self._edge_set = set()

    def add_node(self, node):
        self._nodes[node.node_id] = node

    def add_edge(self, edge):
        if edge.to_node is not None:
            edge_key = (edge.from_node.node_id, edge.to_node.node_id)
            if edge_key not in self._edge_set:
                self._edges.append(edge)
                self._edge_set.add(edge_key)
        else:
            self._edges.append(edge)

    def get_neighbors(self, node_id: str):
        return [
            e.to_node
            for e in self._edges
            if e.from_node.node_id == node_id and e.to_node is not None
        ]

    @property
    def nodes(self):
        return list(self._nodes.values())

    @property
    def edges(self):
        return self._edges

class JsonDatasource(DataSourcePlugin):
    def name(self) -> str:
        return "JSON Datasource"

    def identifier(self) -> str:
        return "datasource_json"

    def load(self, **kwargs) -> JsonGraph:
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
