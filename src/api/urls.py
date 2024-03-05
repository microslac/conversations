from django.urls import include
from django.urls import re_path as url

from core.views import unauthorized

urlpatterns = [
    url(r"^$", unauthorized, name="403"),
    url(r"^conversations/", include("conversations.router", namespace="conversations")),
]
