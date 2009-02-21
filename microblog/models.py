from django.db import models
from django.contrib.auth import models as auth_models

import tagging
from tagging.fields import TagField
from tagging.models import Tag

import re

class Profile(models.Model):
    friends = models.ManyToManyField('self', related_name='friend_of', symmetrical='false')
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

class Entry(models.Model):
    content = models.CharField(max_length=250)
    post_date = models.DateTimeField('date posted')
    owner = models.ForeignKey(Profile, related_name='entries')
    targets = models.ManyToManyField(Profile, related_name='targeted_entries')
    reply_to = models.ForeignKey('self', related_name='replies', null=True, blank=True, default=None)

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
		tagging.models.Tag.objects.add_tag(self, word[1:])
	    elif keep == -1: # first non-special word is kept
		keep = i
	self.content = ' '.join(words[keep:])

    def __unicode__(self):
	return u'%s says "%s" on %s' % (self.owner.user.username, self.content, self.post_date)

    class Meta(object):
	verbose_name_plural = "entries"

tagging.register(Entry)

