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
    url(r'^users/(?P<username>.*)/(?P<postid>\d+)/$', views.profile, name='microblog_focus_post'),
    url(r'^users/(?P<username>.*)/feed/$', views.feed, name='microblog_feed'),
    url(r'^users/(?P<username>.*)/$', views.profile, name='microblog_profile'),
    url(r'^watch/$', views.watch_self, name='microblog_watch_self'),
    url(r'^post/$', views.postentry, name='microblog_post'),
    url(r'^follow/$', views.follow, name='microblog_follow'),
    url(r'^editprofile/$', views.editprofile, name='microblog_editprofile'),
    url(r'^$', views.index, name='microblog_index'),
)

