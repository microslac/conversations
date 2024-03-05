from django.urls import include
from django.urls import re_path as url
from micro.jango.views import unauthorized

urlpatterns = [
    url(r"^$", unauthorized, name="403"),
    url(r"^", include("conversations.router", namespace="conversations")),
]
