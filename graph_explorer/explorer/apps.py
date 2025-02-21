from django.apps import AppConfig
from platform.shop.use_cases.plugin_recognition import PluginService

datasource_group = 'graph_explorer.datasource'

class ExplorerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_explorer'
    plugin_service = PluginService()

    def ready(self):
        # On application start load all plugins
        self.plugin_service.load_plugins(datasource_group)
