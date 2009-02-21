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

from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from tagging.models import Tag

from microblog.models import Profile, Entry
from microblog.forms import PostEntryForm, FollowForm

def profile(request, username):
    # parse request parameters
    page = request.REQUEST.get('page', 1)
    pagesize = request.REQUEST.get('pagesize', 40)
    start = (page - 1)*pagesize

    # pull data
    user = get_object_or_404(User, username=username)
    profile = Profile.get_or_create(user)
    entries = profile.entries.all()[start:start+pagesize]

    context = {
	'user': user,
	'profile': profile,
	'entries': entries,
    }
    return render_to_response('microblog/profile.html', context)

def showentry(request, username, id):
    entry = get_object_or_404(Entry, owner_username=username, pk=id)

    output = u'entry %s by %s: "%s"' % (id, username, entry.content)
    return HttpResponse(output)

def watch(request, username):
    output = u'feed for %s' % username
    return HttpResponse(output)

@login_required
def postentry(request):
    if request.method == 'POST':
	form = PostEntryForm(request.POST)
	if form.is_valid():
	    profile = Profile.get_or_create(request.user)
	    entry = Entry(owner=profile, content=form.cleaned_data['content'], post_date=datetime.now())
	    entry.save()
	    try:
		entry.parse_post()
		entry.save()
	    except:
		entry.delete()
		raise
	    next = urlresolvers.reverse('microblog_index', kwargs={'posted': '1'})
	    return HttpResponseRedirect(next + "?posted=1")
    else:
	form = PostEntryForm()

    return render_to_response('microblog/postentry.html', { 'form': form })

@login_required
def watch_self(request):
    output = u'feed for self'
    return HttpResponse(output)

@login_required
def follow(request):
    context = {'results': []}
    if request.method == 'POST':
	form = FollowForm(request.POST)
	if form.is_valid():
	    own_profile = Profile.get_or_create(request.user)
	    names = form.cleaned_data['users'].split(' ')
	    newnames = []
	    for name in names:
		user = User.objects.filter(username=name)
		if len(user) == 0:
		    context['results'].append((name, 'No such user'))
		    newnames.append(name)
		else:
		    profile = Profile.get_or_create(user[0])
		    profile.followers.add(own_profile)
		    context['results'].append((name, 'Now followed'))
	    if len(newnames):
		form = FollowForm({'users': ' '.join(newnames)})
	    else:
		form = FollowForm()
    else:
	form = FollowForm()

    context['form'] = form
    return render_to_response('microblog/follow.html', context)

def index(request):
    if request.user.is_authenticated():
	context = {
	    'profile': Profile.get_or_create(request.user),
	    'user': request.user,
	}
	return render_to_response('microblog/index_user.html', context)
    else:
	return render_to_response('microblog/index_guest.html')

