# __author__ = "Aditi Sharma"

from django import forms

from subscription.models import SubscribedUser


class SubscriptionForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True, max_length=255)

    class Meta:
        model = SubscribedUser
        fields = ['email']


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=255)
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Enter your name"
        self.fields['email'].label = "Enter a valid email address:"
        self.fields['subject'].label = "Subject"
        self.fields['message'].label = "Write your message here"