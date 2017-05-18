# __author__ = "Aditi Sharma"

from django.shortcuts import render
from django.http import HttpResponse
from django.http import QueryDict
from oauth2client.contrib.django_util import decorators
from django.views.decorators.csrf import csrf_protect
import base64
import json
from bs4 import BeautifulSoup
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import email
import pypwned

# Create your views here.
from posts.models import UserPost


def getBreaches(request):
    email = request.GET.get('account')
    json_data = json.dumps(pypwned.getAllBreachesForAccount(email=email))
    return HttpResponse(json_data)


def pwnedCheck(request):
    return render(request, 'pwnedCheck.html')


data = {}


@decorators.oauth_required
@csrf_protect
def get_google_alerts(request):
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

    if request.method == 'POST':
        id = QueryDict(request.body).get('id')
        try:
            response = GMAIL.users().messages().delete(userId='wikibreach2017@gmail.com', id=id).execute()
            return HttpResponse("Response on delete of" + id + response)
        except errors.HttpError:
            return HttpResponse("Error occured" + id + response)
    else:
        try:
            response = GMAIL.users().messages().list(userId='wikibreach2017@gmail.com',
                                                     q='googlealerts-noreply@google.com').execute()
            data2 = response['messages']
            for message in data2:
                alert = []
                message_body = GMAIL.users().messages().get(userId='wikibreach2017@gmail.com', id=message['id'],
                                                            format='raw').execute()
                msg_snippet = message_body['snippet']
                msg_snippet_split = msg_snippet.split("⋅")
                alert.append(str(msg_snippet_split[1]))
                msg_str = base64.urlsafe_b64decode(message_body['raw'].encode('UTF-8'))
                mime_msg = email.message_from_bytes(msg_str)
                for part in mime_msg.walk():
                    if part.get_content_type() == 'text/plain':
                        msg = part.get_payload(decode=True)
                        msg_link = str(msg).split("<")[1].split(">")[0]
                        alert.append(msg_link)
                        data[message['id']] = alert

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

        user_posts = UserPost.get_user_posts()
        if user_posts:
            return render(request, 'curation.html', {'messages': data, 'user_posts': user_posts})
        else:
            return render(request, 'curation.html', {'messages': data})


@decorators.oauth_required
@csrf_protect
def delete_google_alert(request, id):
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
        response = GMAIL.users().messages().delete(userId='wikibreach2017@gmail.com', id=id).execute()
        print("Message deleted from gmail and corresponding post created in WikiBreach" + id)
    except errors.HttpError:
        print("Error occurred" + id + response)
