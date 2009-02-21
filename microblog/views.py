from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from microblog.models import Entry
from django.contrib.auth.models import User

def profile(request, username):
    user = get_object_or_404(User, username=username)

    output = u'userpage for %s' % username
    return HttpResponse(output)

def showentry(request, username, id):
    entry = get_object_or_404(Entry, owner_username=username, pk=id)

    output = u'entry %s by %s: "%s"' % (id, username, entry.content)
    return HttpResponse(output)

def friends(request, username):
    output = u'friends of %s' % username
    return HttpResponse(output)

def postentry(request):
    output = u'post entry'
    return HttpResponse(output)

def index(request):
    output = u'index'
    return HttpResponse(output)

