from django.contrib.auth.models import AbstractUser
from django.db import models

PENDING = 0
REJECTED = 1
ACCEPTED = 2


class User(AbstractUser):
    logo = models.ImageField(upload_to='user_logo', null=True, blank=True)


class FriendRequest(models.Model):
    FORMATS = (
        (PENDING, "Отправлено"),
        (REJECTED, "Отклонено"),
        (ACCEPTED, "Принято")
    )


    sender = models.ForeignKey(to=User, related_name='sent_requests', on_delete=models.CASCADE, db_index=True)
    receiver = models.ForeignKey(to=User, related_name='received_requests', on_delete=models.CASCADE, db_index=True)

    status = models.PositiveSmallIntegerField(default=PENDING, choices=FORMATS)

    class Meta:
        unique_together = ('sender', 'receiver')