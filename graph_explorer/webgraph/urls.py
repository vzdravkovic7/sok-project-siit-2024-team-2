from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('plugin/datasource/<str:id>', views.datasource_plugin, name="datasource_plugin"),
    path('plugin/visualizer/<str:id>', views.visualizer_plugin, name="visualizer_plugin"),
    path('layout/simple', views.graph_layout, name="graph_layout"),
    path('upload', views.upload_file, name="upload_file"),
    path('query', views.query_graph, name="query_graph"),
    path('reset', views.reset_graph, name="reset_graph"),
    path('remove_search/<int:index>/', views.remove_search, name="remove_search"),
    path('remove_filter/<int:index>/', views.remove_filter, name="remove_filter"),
]
