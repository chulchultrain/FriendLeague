from django.urls import path

from .view import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<name>/',views.account,name='account'),
    path('champion/<name>/',views.champion,name='champion')
]
