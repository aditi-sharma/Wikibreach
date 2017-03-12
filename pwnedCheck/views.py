from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from oauth2client.contrib.django_util.decorators import oauth_required
import pypwned

# Create your views here.


# @login_required(login_url="login/")
# def home(request):
#     return render(request, "home.html")


# def index(request):
#     return HttpResponse(pypwned.getAllBreachesForAccount(email="aditisharma.b@gmail.com"))


@oauth_required(return_url="oauth2/")
def get_alerts(request):
    service = build(serviceName='gmail', version='v1',
                    http=request.oauth.http,
                    developerKey='AIzaSyAg1waT7IavLA2BhfKTwjvqeUbb9A0F7Z8')
    results = service.users().messages().list(userId='me').execute()['items']
    messages = results.get('messages', [])
    return HttpResponse('Message snippet: %s' % messages)
