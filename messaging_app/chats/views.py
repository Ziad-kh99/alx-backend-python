from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        status = self.request.query_params.get("status")
        filters = self.request.query_params.get("filters")
        conversation_pk = self.kwargs.get("conversation")

        if conversation_pk:
            queryset = queryset.filter(conversation=conversation_pk)

        if status:
            queryset = queryset.filter(status=status)

        if filters == "unread":
            queryset = queryset.filter(is_read=False)

        return queryset

    def create(self, request, *args, **kwargs):
        conversation_pk = self.kwargs.get("conversation")
        request.data["conversation"] = conversation_pk
        return super().create(request, *args, **kwargs)
