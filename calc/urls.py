from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history_view, name='history'),
    path('<path:expression>/', views.calculate, name='calculate'),
]
