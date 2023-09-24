from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.entry, name="page"),
    path("create", views.create, name="create"),
    path('edit/<str:page>', views.edit, name="edit"),
    path("random", views.random, name="random"),
]
