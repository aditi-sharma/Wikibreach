# __author__ = "Aditi Sharma"

from http import client
from django.db import Error

import base64
from django.contrib.auth.models import User
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from googleapiclient import discovery
from googleapiclient import errors
from httplib2 import Http
from jsonpickle import json
from oauth2client.contrib.django_util import decorators
from django.views.decorators.csrf import csrf_protect
from oauth2client import file, client, tools
from dateutil import parser
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from curateGoogleAlerts.views import deleteGoogleAlert
from posts.forms import UserPostForm, PostForm
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from posts.models import Post, Tag, UserPost
from send_alerts import send_email


def _posts(request, posts):
    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'allPosts.html', {
        'posts': posts,
    })


def posts(request):
    all_posts = Post.get_posts()
    return _posts(request, all_posts)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post.html', {'post': post})

@decorators.oauth_required
@csrf_protect
def createPost(request, id):
    global GMAIL
    try:
        store = file.Storage('WikiBreach/gmail.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('WikiBreach/client_secret.json',
                                                  'https://mail.google.com/')
            creds = tools.run_flow(flow, store)
        GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

    try:
        message_body = GMAIL.users().messages().get(userId='wikibreach2017@gmail.com', id=id).execute()
        data = message_body['payload']
        msg = data['parts']
        part = msg[1]
        body = part['body']
        dat = body['data']
        msg_str = base64.urlsafe_b64decode(dat.encode('UTF-8'))
        soup = BeautifulSoup(msg_str, "lxml")
        d = str(soup.find_all("script"))
        m = []
        m = d.split("type=\"application/json\">", 1)
        p = m[1].split("</script>]", 1)
        msg_json = str(p[0])
        data2 = json.loads(msg_json)
        date = data2['entity']['subtitle']
        dateArray = date.split("Latest: ")
        date = dateArray[1]
        date = parser.parse(date).strftime('%Y-%m-%d')
        keyword = str(data2['entity']['title']).split("Google Alert - ")[1]
        widgets = data2["cards"][0]
        widgets = widgets['widgets'][0]
        title = widgets['title']
        description = widgets['description']
        source_url = widgets['url']
        return render(request, 'createPost.html',
                      {'title': title, 'date': date, 'keyword': keyword, 'description': description,
                       'sourcelink': source_url, 'message_id': id})
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


@login_required
def publishPost(request, id):
    form = PostForm(request.POST)
    if form.is_valid():
        post = Post()
        post.title = form.cleaned_data.get('title')
        post.content = form.cleaned_data.get('content')
        post.source_url = form.cleaned_data.get('source_url')
        post.breach_date = form.cleaned_data.get('breach_date')
        user = form.cleaned_data.get('created_by_user')
        if user:
            post.create_user = User.objects.get(username=user)
        else:
            post.create_user = request.user
        try:
            post.save()
            tags = form.cleaned_data.get('tags')
            post.create_tags(tags)
            breach_alert = get_object_or_404(Post, title=post.title, breach_date=post.breach_date)
            send_email(breach_alert.title, breach_alert.slug)
            if id:
                deleteGoogleAlert(request, id)
            return redirect('post', slug=breach_alert.slug)
        except Error:
            return HttpResponse(Error)
    else:
        return HttpResponse(form.errors)


def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    posts = []
    for tag in tags:
        posts.append(tag.post)
    return posts(request, posts)


def editPost(request, slug):
    tags = []
    post = get_object_or_404(Post, slug=slug)
    for tag in post.get_tags():
        tags.append(str(tag))
    tagString = " ".join(tags)
    date = parser.parse(str(post.breach_date)).strftime('%Y-%m-%d')
    return render(request, 'editPost.html', {'post': post, 'tags': tagString, 'date': date})


def updatePost(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/posts/')
        else:
            return HttpResponse("Error occurred")


def deletePost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('/posts/')


def user_post(request, id):
    post = get_object_or_404(UserPost, id=id)
    date = parser.parse(str(post.breach_date)).strftime('%Y-%m-%d')
    title = post.title
    tags = post.tags
    content = post.content
    source_url = post.source_url
    user = post.create_user
    post.delete()
    return render(request, 'createPost.html',
                  {'title': title, 'date': date, 'keyword': tags, 'description': content,
                   'sourcelink': source_url, 'by_user': user})


def delete_user_post(request):
    try:
        id = QueryDict(request.body).get('id')
        post = get_object_or_404(UserPost, id=id)
        post.delete()
        return HttpResponse("User post deleted")
    except errors.HttpError:
        return HttpResponse("Error occured" + id + post.title)


def contribute(request):
    if request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            post = UserPost()
            post.title = form.cleaned_data.get('title')
            post.content = form.cleaned_data.get('content')
            post.source_url = form.cleaned_data.get('source_url')
            post.breach_date = form.cleaned_data.get('breach_date')
            post.create_user = request.user
            post.tags = form.cleaned_data.get('tags')
            post.save()
            return render(request, 'user_submitted_post.html', {'post_success': True, 'form': UserPostForm()})
        else:
            return render(request, 'user_submitted_post.html',
                          {'form': form})
    else:
        return render(request, 'user_submitted_post.html',
                      {'form': UserPostForm()})
