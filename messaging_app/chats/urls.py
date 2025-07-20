from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

messages_router = NestedDefaultRouter(router, r"conversations", lookup="conversation")
router.register(r"messages", MessageViewSet, basename="conversation_messages")

urlpatterns = [path("", include(router.urls)), path("", include(messages_router.urls))]
