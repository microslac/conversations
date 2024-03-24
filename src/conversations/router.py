from django.conf import settings
from django.urls import include
from django.urls import re_path as url
from rest_framework import routers

from conversations.views import ConversationViewSet, InternalViewSet

app_name = settings.APP_CONVERSATIONS
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"internal", InternalViewSet, basename="internal")

urlpatterns = [
    url(r"^", include(router.urls)),
]
