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

from django.db import models
from django.db.models import Q
from django.contrib.auth import models as auth_models
from django.core import exceptions
from django.conf import settings
from django.template import Context, loader

import tagging
from tagging.fields import TagField
from tagging.models import Tag

import re

import xmlrpclib

try:
    idavoll = xmlrpclib.ServerProxy(settings.IDAVOLL_XMLRPC_SERVICE)
except KeyError:
    raise exceptions.ImproperlyConfigured(
	'microblog-demo needs IDAVOLL_XMLRPC_SERVICE in settings.py')

class Profile(models.Model):
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    user = models.OneToOneField(auth_models.User, related_name='microblog_profile')
    jid = models.CharField(max_length="255", blank=True)

    def feed(self):
	followed = Q(owner__followers = self)
	targeted = Q(targets = self)
	return Entry.objects.filter(followed | targeted)

    def __unicode__(self):
	return u'%s' % self.user.username

    class Meta:
	ordering = [ 'user__username' ]

class Entry(models.Model):
    content = models.CharField(max_length=140)
    post_date = models.DateTimeField('date posted')
    owner = models.ForeignKey(Profile, related_name='entries')
    targets = models.ManyToManyField(Profile, related_name='targeted_entries')

    def get_tags(self):
	return Tag.objects.get_for_object(self)

    def parse_post(self):
	''' parse_post(): Parse a post for @target and #tag syntax
	'''
	words = self.content.split(' ')
	for i, word in enumerate(words):
	    if word.startswith('@'):
		users = Profile.objects.filter(user__username = word[1:])
		if len(users) == 0:
		    continue # TODO: spit error
		self.targets.add(users[0])
	    elif word.startswith('#'):      # tag this entry
		Tag.objects.add_tag(self, word[1:])

    def publish(self):
	''' publish(): Publish entry to XMPP Pubsub over XMLRPC to idavoll
	'''
	
	username = self.owner.user.username
	entryDetails = Context({
	    'text': self.content,
	    'id': self.id,
	    'date': self.post_date.isoformat(),
	    'author': username,
	    'tags': [tag.name for tag in self.tags]
	})
	template = loader.get_template("microblog/entry.atom")
	atomxml = unicode(template.render(entryDetails))
	message = loader.get_template("microblog/entry.message").render(entryDetails)

	print "Publishing %s" % self.id
	print atomxml

	try:
	    # TODO: don't resend this, split off on the other end after parsing once!
	    idavoll.publish('user/%s' % username, str(self.id), atomxml)
	    for follower in self.owner.followers.all():
		idavoll.publish('feed/%s' % follower.user.username, str(self.id), atomxml)
		if follower.jid:
		    idavoll.message(follower.jid, unicode(message))
	    for tag in self.tags:
		idavoll.publish('tag/%s' % tag.name, str(self.id), atomxml)
	except xmlrpclib.Fault, f:
	    print "publishing entry %s: %s" % (self.id, f)
	    #ignore

    def __unicode__(self):
	return u'%s says "%s" on %s' % (self.owner.user.username, self.content, self.post_date)

    class Meta(object):
	verbose_name_plural = "entries"
	ordering = ['-post_date']
	get_latest_by = 'post_date'

tagging.register(Entry)

