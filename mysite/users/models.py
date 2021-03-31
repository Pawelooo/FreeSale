from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    phone = models.CharField(max_length=11, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info', null=True)
    image = models.ImageField(blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('15'))

    def __str__(self):
        return f'{UserInfo}'


class Conversation(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')


class Message(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)


