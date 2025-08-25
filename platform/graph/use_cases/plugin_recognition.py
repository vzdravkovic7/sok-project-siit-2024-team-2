import pkg_resources
from typing import Dict, List, Type

from graph.api.services.plugin import DataSourcePlugin, VisualizerPlugin

DATASOURCE_GROUP = "graph.datasource"
VISUALIZER_GROUP = "graph.visualizer"

class PluginService:
    """Service for discovering and managing graph plugins.

    The `PluginService` loads and stores plugin instances defined
    in entry points. Two types of plugins are supported:
    - Datasource plugins (group: `graph.datasource`).
    - Visualizer plugins (group: `graph.visualizer`).

    Plugins are expected to inherit from either `DataSourcePlugin`
    or `VisualizerPlugin` depending on their group.
    """

    def __init__(self):
        """Initializes an empty plugin registry.

        Attributes:
            plugins (dict[str, list]): Dictionary that stores lists of
                loaded plugin instances for each group.
        """
        self.plugins: Dict[str, List] = {
            DATASOURCE_GROUP: [],
            VISUALIZER_GROUP: []
        }

    def load_plugins(self):
        """Discovers and loads all available plugins.

        Uses `pkg_resources.iter_entry_points` to find plugins registered
        in the `graph.datasource` and `graph.visualizer` groups. Each
        discovered class is instantiated and stored in the internal registry.

        Example:
            >>> ps = PluginService()
            >>> ps.load_plugins()
            >>> len(ps.plugins[DATASOURCE_GROUP]) > 0
            True
        """
        self.plugins[DATASOURCE_GROUP] = self._load_plugins(DATASOURCE_GROUP, DataSourcePlugin)
        self.plugins[VISUALIZER_GROUP] = self._load_plugins(VISUALIZER_GROUP, VisualizerPlugin)

    def _load_plugins(self, group: str, base_class: Type):
        """Helper method to load plugins from a specific group.

        Args:
            group (str): The entry point group name (`graph.datasource` or `graph.visualizer`).
            base_class (Type): The expected base class (`DataSourcePlugin` or `VisualizerPlugin`).

        Returns:
            list: A list of instantiated plugin objects.
        """
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
        """Retrieves a plugin instance by group and identifier.

        Args:
            group (str): Plugin group (`graph.datasource` or `graph.visualizer`).
            identifier (str): The unique identifier of the plugin.

        Returns:
            object | None: The matching plugin instance if found, otherwise `None`.

        Example:
            >>> ps = PluginService()
            >>> ps.load_plugins()
            >>> plugin = ps.get_plugin(DATASOURCE_GROUP, "datasource_json")
            >>> plugin.name()
            'JSON Datasource'
        """
        for plugin in self.plugins.get(group, []):
            if plugin.identifier() == identifier:
                return plugin
        return None
