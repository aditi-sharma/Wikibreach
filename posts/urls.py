from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^$', views.posts,  name='posts'),
    url(r'^createPost/(?P<id>\w+)/$', views.createPost, name='createPost'),
    url(r'^publishPost/', views.publishPost, name='publishPost'),
    url(r'^(?P<slug>[-\w]+)/$', views.post, name='post'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.editPost, name='edit'),
    url(r'^update/(?P<slug>[-\w]+)/$', views.updatePost, name='update'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.deletePost, name='delete'),
]
