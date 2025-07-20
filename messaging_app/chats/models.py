from django.db import models
import uuid


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=225)
    phone_number = models.IntegerField()
    password = models.CharField()


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ForeignKey(User, on_delete=models.CASCADE)
    StartedAt = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_body = models.CharField(max_length=225)
    status = models.CharField(
        max_length=50, choices=[("sent", "Sent"), ("delivered", "Delivered")]
    )
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_created=True)
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
