from django.apps import AppConfig
from graph.use_cases.plugin_recognition import PluginService

datasource_group = 'graph.datasource'

class ExplorerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webgraph'
    plugin_service = PluginService()

    def ready(self):
        # On application start load all plugins
        self.plugin_service.load_plugins(datasource_group)
