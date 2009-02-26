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

from twisted.web import xmlrpc, server
from twisted.internet import defer
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.words.xish.domish import elementStream
from twisted.words.protocols.jabber import jid

from wokkel.pubsub import Item

from idavoll import error

class XMLRPC(xmlrpc.XMLRPC):

    def __init__(self, backend, owner):
	xmlrpc.XMLRPC.__init__(self)
	self.backend = backend
	self.owner = owner

    @inlineCallbacks
    def xmlrpc_create(self, nodeid):
	print "Creating node %s..." % nodeid
	realnodeid = yield self.backend.createNode(nodeid, self.owner)
	returnValue(realnodeid)

    @inlineCallbacks
    def xmlrpc_publish(self, nodeid, itemid, itemxml):
	try:
	    nodeid = yield self.backend.createNode(nodeid, self.owner)
	except error.NodeExists:
	    pass
	items = [Item(itemid, itemxml)]

	yield self.backend.publish(nodeid, items, self.owner)
	returnValue(nodeid)

