from importlib.metadata import entry_points
from typing import List, Dict
from graph.api.services import DataSourcePlugin

class PluginService:
    def __init__(self):
        self.plugins: Dict[str, List[DataSourcePlugin]] = {}

    def load_plugins(self, group: str):
        """
        Dynamically loads plugins based on entrypoint group.
        """
        self.plugins[group] = []
        for ep in entry_points(group=group):
            p = ep.load()
            plugin: DataSourcePlugin = p()
            self.plugins[group].append(plugin)
