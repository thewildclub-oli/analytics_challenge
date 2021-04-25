from django.urls import path

from . import views

app_name="analytics_component"

urlpatterns=[
    path('', views.index, name='index')
]