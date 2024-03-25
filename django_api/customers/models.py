from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from customers.validation import CustomEmailValidator


def user_logo_path(instance, filename):
    username = instance.username
    return f'logos/{username}/{filename}'


class UserInfo(models.Model):

    user_course_lvl = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    user_variant = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(35)]
    )

    FACULTY_CHOICES = [
        ('IKTA', 'Faculty of IKTA'),
        ('IKHI', 'Faculty of IKHI'),
        ('IAДУ', 'Faculty of IAДУ'),
        ('IАРД', 'Faculty of IАРД'),
        ('ІБІС', 'Faculty of ІБІС'),
        ('ІГДГ', 'Faculty of ІГДГ'),
        ('ІГСН', 'Faculty of ІГСН'),
        ('ІНЕМ', 'Faculty of ІНЕМ'),
        ('IЕСК', 'Faculty of ІЕСК'),
        ('ІППТ', 'Faculty of ІППТ'),
        ('ІППО', 'Faculty of ІППО'),
        ('ІМФН', 'Faculty of ІМФН'),
        ('ІСТР', 'Faculty of ІСТР'),
        ('ІТРЕ', 'Faculty of ІТРЕ'),
        ('IXXT', 'Faculty of IXXT'),
        ('IAДУ', 'Faculty of IXXT'),
    ]

    user_faculty = models.CharField(
        max_length=4,  # Adjust the max length based on your requirements
        choices=FACULTY_CHOICES,
        blank=True,
        null=True,
    )



class Account(AbstractUser):
    logo = models.ImageField(upload_to=user_logo_path, blank=True, null=True)
    email = models.EmailField(
        validators=[
            CustomEmailValidator(
                message="Incorrect email, check if it ends with: lpnu.ua, other university",
                code=None,
                allowlist=("lpnu.ua",)
            )
        ],
        unique=True,
        error_messages={
            "unique": ("You've already registered"),
        },
    )
    # is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    user_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE, blank=True, null=True, default=None)
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """Save the user, hash the password if it's set."""
        if not self.is_superuser:  # Only hash the password if it's a new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    groups = None
    user_permissions = None


class UserRating(models.Model):
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="creatorID")
    userID = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="userID")
    rating = models.PositiveIntegerField(choices=[(1, '1 start'),
                                                  (2, '2 starts'),
                                                  (3, '3 starts'),
                                                  (4, '4 starts'),
                                                  (5, '5 starts')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('creator', 'userID')
