# __author__ = "Aditi Sharma"

from django.core.exceptions import ValidationError
from django import forms
from datetime import datetime
from django.core.validators import URLValidator
from posts.models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=255)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)
    source_url = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=300)
    breach_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False)
    created_by_user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      max_length=25, required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'source_url', 'breach_date', 'tags']


def DateValidator(value):
    print(value)
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except:
        raise ValidationError('Enter a valid date of the format YYYY-mm-dd')


def SourceUrlValidator(value):
    validator = URLValidator()
    try:
        validator(value)
    except:
        raise ValidationError("Enter the source url in a valid format")


class UserPostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=150)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True,
        max_length=500)
    source_url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=100)
    breach_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        help_text='Date should be of the format <strong>YYYY-MM-DD</strong>')
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=25, required=False,
        help_text='Specify tags in double-quotes, and Use spaces to separate the tags, such as "data-breach ransomware"')

    class Meta:
        model = Post
        fields = ['title', 'content', 'source_url', 'breach_date', 'tags']

    def __init__(self, *args, **kwargs):
        super(UserPostForm, self).__init__(*args, **kwargs)
        self.fields['source_url'].validators.append(SourceUrlValidator)
        self.fields['source_url'].label = "Link to the Source"
        self.fields['breach_date'].label = "Date of Breach"

    def clean(self):
        super(UserPostForm, self).clean()
