from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login/", views.login, name="login"),
    path("<int:tweet_id>/", views.annotate, name="annotate"),
    path("data/", views.data, name="data"),
    path("data/download/", views.download, name="download"),
]
