# __author__ = "Aditi Sharma"

from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^$', views.posts,  name='posts'),
    url(r'^contribute/', views.contribute,  name='contribute'),
    url(r'^createPost/(?P<id>\w+)/$', views.create_post, name='createPost'),
    url(r'^createUserPost/(?P<id>[-\w]+)/$', views.user_post, name='createUserPost'),
    url(r'^publishPost/(?P<id>[-\w]+)/$', views.publish_post, name='publishPost'),
    url(r'^(?P<slug>[-\w]+)/$', views.post, name='post'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit_post, name='edit'),
    url(r'^update/(?P<slug>[-\w]+)/$', views.update_post, name='update'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete_post, name='delete'),

]
