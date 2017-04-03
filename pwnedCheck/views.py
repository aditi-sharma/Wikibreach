from django.shortcuts import render
from django.shortcuts import HttpResponse
import pypwned
from oauth2client.contrib.django_util import decorators
import base64
import json
# Create your views here.



def home(request):
    return render(request, "base.html")

snippet = []
@decorators.oauth_required
def get_profile_required(request):
    resp, messages = request.oauth.http.request('https://www.googleapis.com/gmail/v1/users/wikibreach2017@gmail.com/messages')
    json_data = json.loads(messages)
    data = json_data['messages']
    for message in data:
        id = message['id']
        resp1, content = request.oauth.http.request('https://www.googleapis.com/gmail/v1/users/wikibreach2017@gmail.com/messages/' + id)
        message_data = json.loads(content)
        payload = message_data['payload']
        parts = payload['parts']

        # snippet.append(base64.b64decode(data2))
       # return HttpResponse(body)
