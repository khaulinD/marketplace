from django.db import models
from django.contrib.auth import get_user_model

from customers.models import Account


# class Conversation(models.Model):
#     channel_id = models.CharField(max_length=255)
#     create_at = models.DateTimeField(auto_now_add=True)
#
#
# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(Account, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#


from django.contrib.auth import get_user_model
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sender.username}-{self.thread_name}' if self.sender else f'{self.message}-{self.thread_name}'