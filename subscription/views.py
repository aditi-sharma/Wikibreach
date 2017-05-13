from django.shortcuts import render

# Create your views here.
from posts.models import Post
from subscription.forms import SubscriptionForm
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
    except Exception:
        return render(request, 'subscribed.html', {'exists': False, 'error': True, 'posts': all_posts})