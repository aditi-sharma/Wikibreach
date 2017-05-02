__author__ = "Aditi Sharma"

from django import forms

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
       # help_text='Use spaces to separate the tags, such as "java jsf primefaces"')  # noqa: E501

    class Meta:
        model = Post
        fields = ['title', 'content', 'source_url', 'breach_date', 'tags']
