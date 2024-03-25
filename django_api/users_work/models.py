from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from customers.models import Account


class UserWork(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    creatorID = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ExtraWorkInfo(models.Model):
    workID = models.OneToOneField(UserWork, on_delete=models.CASCADE, primary_key=True, related_name='extra_info')
    work_course_lvl = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    work_subject_name = models.CharField(max_length=50, blank=False, null=False)
    work_subject_teacher = models.CharField(max_length=50, blank=False, null=False)