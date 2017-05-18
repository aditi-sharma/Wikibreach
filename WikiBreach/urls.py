"""WikiBreach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from authentication.forms import LoginForm
from django.conf import urls
import oauth2client.contrib.django_util.site as django_util_site
from curateGoogleAlerts import views as view
from authentication import views as auth_views
from posts import views as home
from search import views as search_views
from subscription import views as subscribe_views

urlpatterns = [
    url(r'^$', home.posts, name='home'),
    url(r'^signup/$', auth_views.signup, name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^getAlerts/', view.get_profile_required, name='getAlerts'),
    url(r'^posts/', include('posts.urls')),
    url(r'^search', search_views.search, name='search'),
    url(r'^pwnedCheck/', view.pwnedCheck, name='pwnedCheck'),
    url('^subscribe/', subscribe_views.subscribe, name='subscribe'),
    url('^contactUs/', subscribe_views.contactUs, name='contactUs'),
    url('^aboutUs/', subscribe_views.aboutUs, name='aboutUs'),
    url(r'^getBreaches/', view.getBreaches),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^oauth2/', urls.include(django_util_site.urls)),
    url(r'^rejectUserPost/', home.delete_user_post, name='rejectUserPost'),

]
