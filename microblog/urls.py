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

from django.conf.urls.defaults import *

from microblog import views

urlpatterns = patterns('',
    url(r'^users/(?P<username>.*)/friends/$', views.friends, name='microblog_friends'),
    url(r'^users/(?P<username>.*)/(?P<id>\d+)/$', views.showentry, name='microblog_entry'),
    url(r'^users/(?P<username>.*)/(?P<id>\d+)/reply$', views.showentry, name='microblog_entry_reply'),
    url(r'^users/(?P<username>.*)/$', views.profile, name='microblog_profile'),
    (r'^post/$', views.postentry),
    (r'^$', views.index),
)

