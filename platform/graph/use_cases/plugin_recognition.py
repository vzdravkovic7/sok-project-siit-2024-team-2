import importlib
import pkg_resources
from typing import Dict, List, Type

from graph.api.services.plugin import DataSourcePlugin, VisualizerPlugin

DATASOURCE_GROUP = "graph.datasource"
VISUALIZER_GROUP = "graph.visualizer"


class PluginService:
    def __init__(self):
        self.plugins: Dict[str, List] = {
            DATASOURCE_GROUP: [],
            VISUALIZER_GROUP: []
        }
        self.load_plugins()

    def load_plugins(self):
        self.plugins[DATASOURCE_GROUP] = self._load_plugins(DATASOURCE_GROUP, DataSourcePlugin)
        self.plugins[VISUALIZER_GROUP] = self._load_plugins(VISUALIZER_GROUP, VisualizerPlugin)

    def _load_plugins(self, group: str, base_class: Type):
        loaded_plugins = []
        for entry_point in pkg_resources.iter_entry_points(group):
            try:
                plugin_class = entry_point.load()
                if issubclass(plugin_class, base_class):
                    loaded_plugins.append(plugin_class())
            except Exception as e:
                print(f"Failed to load plugin {entry_point.name}: {e}")
        return loaded_plugins

    def get_plugin(self, group: str, identifier: str):
        for plugin in self.plugins.get(group, []):
            if plugin.identifier() == identifier:
                return plugin
        return None
