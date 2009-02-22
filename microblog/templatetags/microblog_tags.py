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

from django import template

import microblog.forms

register = template.Library()

@register.filter
def fill_microblog_entry(entry, user):
    try:
        entry.replyform = microblog.forms.PostEntryForm(auto_id='reply%s_%%s' % entry.pk)
        entry.to_you = user.is_authenticated() and entry.targets.filter(user = user).count() > 0
	if not hasattr(entry, 'highlight'):
	    entry.highlight = False
    except:
	print "Failure in fill_microblog:"
	import traceback
	traceback.print_exc()
    return entry

@register.filter
def fill_microblog_feed(feed, user):
    for entry in feed:
	yield fill_microblog_entry(entry, user)

