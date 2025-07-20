from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    conversations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Conversation.objects.all()
    )

    class Meta:
        model = User
        fields = ("user_id", "first_name", "last_name", "conversations")


class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(
        max_length=225
    )  # used for input (post & update)
    preview = serializers.SerializerMethodField()  # used for output (get)

    class Meta:
        model = Message
        fields = (
            "message_id",
            "message_body",
            "preview",
            "sender",
            "conversation",
            "is_read",
            "status",
        )

    def get_preview(self, obj):
        return obj.message_body[:30]

    def validate(self, data):
        """
        data is the value of fields & when call is_valid() data be like:
        {
        "message_body": "hello world",
        "sender": <User instance>,  -----> convert to model
        "conversation": <Conversation instance> -----> convert to model
        }
        """
        if data["sender"] not in data["conversation"].participants.all():
            raise serializers.ValidationError(
                "Sender must be part of the conversation."
            )
        return data


class ConversationSerializer(serializers.ModelSerializer):

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages"]
