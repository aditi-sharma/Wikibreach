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
from pwnedCheck.forms import LoginForm
from django.conf import urls
import oauth2client.contrib.django_util.site as django_util_site
from pwnedCheck import views as view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getAlerts', view.get_profile_required),
    url(r'^posts/', include('posts.urls')),
    url(r'^pwnedCheck/', view.pwnedCheck),
    url(r'^getBreaches/', view.getBreaches),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^oauth2/', urls.include(django_util_site.urls)),

]
