from django.shortcuts import render
from django.http import HttpResponse
from django.http import QueryDict
import html2text
from oauth2client.contrib.django_util import decorators
from django.views.decorators.csrf import csrf_protect
import base64
import json
import requests
from bs4 import BeautifulSoup
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import email
# Create your views here.



def home(request):
    return render(request, "base.html")

data = {}
@decorators.oauth_required
@csrf_protect
def get_profile_required(request):
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
            return HttpResponse("Response on delete of"+ id + response)
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
    else:
        try:
            response = GMAIL.users().messages().list(userId='wikibreach2017@gmail.com').execute()
            data2 = response['messages']
            for message in data2:
                alert = []
                message_body = GMAIL.users().messages().get(userId='wikibreach2017@gmail.com',id=message['id'],format='raw').execute()
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

            return render(request, 'curation.html', {'messages': data})

        except errors.HttpError as error:
            print('An error occurred: %s' % error)


@decorators.oauth_required
@csrf_protect
def view_posts(request):
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
        response = GMAIL.users().messages().list(userId='wikibreach2017@gmail.com').execute()
        data2 = response['messages']
        for message in data2:
            message_body = GMAIL.users().messages().get(userId='wikibreach2017@gmail.com', id=message['id'],
                                                        format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message_body['raw'].encode('UTF-8'))
            mime_msg = email.message_from_bytes(msg_str)
            return render(request, 'home.html', {'part': mime_msg})

    except errors.HttpError as error:
        print('An error occurred: %s' % error)

