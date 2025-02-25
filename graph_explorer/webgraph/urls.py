from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('plugin/datasource/<str:id>', views.datasource_plugin, name="datasource_plugin"),
    path('plugin/visualizer/<str:id>', views.visualizer_plugin, name="visualizer_plugin"),
    path('layout/simple', views.graph_layout, name="graph_layout"),
]