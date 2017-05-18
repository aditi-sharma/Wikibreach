# __author__ = "Aditi Sharma"

from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from WikiBreach.settings import ADMIN_EMAIL, CONTACT_EMAIL
from posts.models import Post
from subscription.forms import SubscriptionForm, ContactForm
from subscription.models import SubscribedUser


def subscribe(request):
    all_posts = Post.get_posts()
    form = SubscriptionForm(request.POST)
    for field in form:
        if field.errors:
            return render(request, 'subscribed.html', {'exists': True, 'error': False, 'posts': all_posts})
    try:
        if form.is_valid():
            email = form.cleaned_data.get('email')
            SubscribedUser.subscribe(email=email)
            return render(request, 'subscribed.html', {'exists': False, 'error': False, 'posts': all_posts})
        else:
            return render(request, 'subscribed.html', {'exists': False, 'error': True, 'posts': all_posts})
    except Exception as E:
        return render(request, 'subscribed.html', {'exists': False, 'error': True, 'posts': all_posts})


def contactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        try:
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                subject = form.cleaned_data.get('subject')
                message = "A WikiBreach user " + name + "has sent the following message:" + "\n \n"
                message += form.cleaned_data.get('message')
                message += "\n \n You can reply to this message by emailing the user at: " + email
                send_mail(subject, message, ADMIN_EMAIL, [CONTACT_EMAIL])
                print(" User contact Email sent to " + CONTACT_EMAIL)
                return render(request, 'contactUs.html', {'message_submitted': True, 'form': ContactForm()})
        except Exception as E:
            return render(request, 'contactUs.html', {'message_submitted': False, 'form': form})
    else:
        return render(request, 'contactUs.html', {'form': ContactForm()})


def aboutUs(request):
    return render(request, 'aboutUs.html')