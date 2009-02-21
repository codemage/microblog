""" Copyright (c) 2009 Walter Mundt

    This file is part of microblogging-demo.

    microblogging-demo is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    microblogging-demo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with microblogging-demo.  If not, see <http://www.gnu.org/licenses/>.
"""

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

