from django.urls import path

from . import views

app_name = 'cargas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cargas/', views.lista, name='lista'),
    path('cargas/nova/', views.criar, name='criar'),
    path('cargas/<int:pk>/', views.detalhe, name='detalhe'),
    path('cargas/<int:pk>/editar/', views.editar, name='editar'),
    path('cargas/<int:pk>/excluir/', views.excluir, name='excluir'),
]
