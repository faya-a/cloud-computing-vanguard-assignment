from django.urls import path

from storage.api import api

urlpatterns = [
    path("/", view=api.urls, name="storage"),
]
