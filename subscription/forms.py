__author__ = "Aditi Sharma"

from django import forms

from subscription.models import SubscribedUser


class SubscriptionForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True, max_length=255)

    class Meta:
        model = SubscribedUser
        fields = ['email']