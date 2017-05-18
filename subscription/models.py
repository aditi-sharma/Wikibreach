# __author__ = "Aditi Sharma"

from django.db import models


# Create your models here.
class SubscribedUser(models.Model):
    email = models.EmailField(max_length=255, primary_key=True, blank=False, null=False)
    is_active = models.BooleanField(max_length=5, blank=False, null=False, default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SubscribedUser"
        verbose_name_plural = "SubscribedUsers"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    @staticmethod
    def get_emails():
        email_list = SubscribedUser.objects.filter(is_active=True)
        emails = email_list.values_list('email', flat=True)
        return emails

    @staticmethod
    def subscribe(email):
        user, created = SubscribedUser.objects.get_or_create(email=email)

    @staticmethod
    def unsubscribe(email):
        SubscribedUser.objects.filter(email=email).update(is_active=False)
