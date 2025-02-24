from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('plugin/datasource/<str:id>', views.datasource_plugin, name="datasource_plugin"),
    path('layout/tree', views.graph_layout, name="graph_layout"),
]