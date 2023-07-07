from django.urls import path
from . import views

urlpatterns = [
    path("git_webhook/", views.git_webhook, name="git_webhook"),
]
