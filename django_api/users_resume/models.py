from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from customers.models import Account




class Resume(models.Model):

    title = models.CharField(max_length=255, blank=False, null=False)
    creatorID = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.IntegerField(blank=False, null=False)
    amount_orders = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ExtraResumeInfo(models.Model):
    resumeID = models.OneToOneField(Resume, on_delete=models.CASCADE, primary_key=True, related_name='extra_info')
    resume_course_lvl = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )


