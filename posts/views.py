from http import client

import base64
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from googleapiclient import discovery
from googleapiclient import errors
from httplib2 import Http
from jsonpickle import json
from oauth2client.contrib.django_util import decorators
from django.views.decorators.csrf import csrf_protect
from oauth2client import file, client, tools
from dateutil import parser
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from posts.forms import PostForm
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from posts.models import Post, PostComment, Tag


def _posts(request, posts):
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'allPosts.html', {
        'posts': posts,
        'popular_tags': popular_tags
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
                       'sourcelink': source_url})
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


@login_required
def publishPost(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = Post()
        post.title = form.cleaned_data.get('title')
        post.content = form.cleaned_data.get('content')
        post.source_url = form.cleaned_data.get('source_url')
        post.breach_date = form.cleaned_data.get('breach_date')
        post.save()
        tags = form.cleaned_data.get('tags')
        post.create_tags(tags)
        return render(request, 'allPosts.html')
    else:
        return HttpResponse("Error occurred")


def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    posts = []
    for tag in tags:
            posts.append(tag.post)
    return posts(request, posts)


def editPost(request, slug,):
    tags = []
    post = get_object_or_404(Post, slug=slug)
    for tag in post.get_tags():
        tags.append(str(tag))
    tagString = " ".join(tags)
    return render(request, 'editPost.html', {'post': post, 'tags': tagString})



def updatePost(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # form.save()
            return HttpResponse(form)
        else:
            return HttpResponse("Error occurred")