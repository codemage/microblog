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
from django.contrib.auth import models as auth_models

import tagging
from tagging.fields import TagField
from tagging.models import Tag

import re

class Profile(models.Model):
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    user = models.OneToOneField(auth_models.User, related_name='microblog_profile')

    def __unicode__(self):
	return u'%s' % self.user.username

    @classmethod
    def get_or_create(cls, user):
	try:
	    return user.microblog_profile
	except cls.DoesNotExist:
	    p = Profile(user=user)
	    p.save()
	    return p
    
    class Meta:
	ordering = [ 'user__username' ]

class Entry(models.Model):
    content = models.CharField(max_length=250)
    post_date = models.DateTimeField('date posted')
    owner = models.ForeignKey(Profile, related_name='entries')
    targets = models.ManyToManyField(Profile, related_name='targeted_entries')
    reply_to = models.ForeignKey('self', related_name='replies', null=True, blank=True, default=None)

    def get_tags(self):
	return Tag.objects.get_for_object(self)

    def parse_post(self):
	''' parse_post(): Parse a post for @target and #tag syntax

	Remove from the text any such words that appear at the beginning.
	'''
	words = self.content.split(' ')
	keep = -1 # if changed, remove words before this
	for i, word in enumerate(words):
	    if word.startswith('@'):
		if re.match(word, r'@\d+'): # reply to specific entry
		    entries = Entry.objects.filter(pk = int(word[1:]))
		    if len(entries) == 0:
			continue # TODO: spit error
		    self.reply_to = entries[0]
		else:                       # reply to person
		    users = Profile.objects.filter(user__username = word[1:])
		    if len(users) == 0:
			continue # TODO: spit error
		    self.targets.add(user[0])
	    elif word.startswith('#'):      # tag this entry
		Tag.objects.add_tag(self, word[1:])
	    elif keep == -1: # first non-special word is kept
		keep = i
	self.content = ' '.join(words[keep:])

    def __unicode__(self):
	return u'%s says "%s" on %s' % (self.owner.user.username, self.content, self.post_date)

    class Meta(object):
	verbose_name_plural = "entries"
	ordering = ['-post_date']
	get_latest_by = 'post_date'

tagging.register(Entry)

