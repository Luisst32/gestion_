from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='producto_list'),
    path('crear/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_delete'),
]
