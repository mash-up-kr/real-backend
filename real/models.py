from django.db import models
from django.utils import timezone
from member.models import User

DREAM_TAG = (
    (0, 'CAN DO'),
    (1, 'CAN PLAY'),
    (2, 'CAN GO'),
    (3, 'CAN MAKE'),
    (4, 'CAN EAT'),
)


class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField()
    start_at = models.DateField()
    complete_by = models.DateField()
    tag = models.IntegerField(choices=DREAM_TAG)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Result(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)
    complete_at = models.DateField()
    review = models.TextField(blank=True)
    photo = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dream.title
