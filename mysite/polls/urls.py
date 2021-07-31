from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mynewview/', views.my_new_view, name='mynewview'),
]
