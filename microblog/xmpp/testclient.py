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

from twisted.words.xish import domish
from twisted.application import service
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.words.protocols.jabber import jid

from wokkel import pubsub, client, xmppim

botjid = jid.internJID('test@lerran.apogean.org/testbot')
botpass = 'secret'
admin = jid.internJID('waltermundt@lerran.apogean.org')
pubsubService = 'pubsub.lerran.apogean.org'

class BotMessageProtocol(xmppim.MessageProtocol):
    def __init__(self, ownjid, adminjid):
	xmppim.MessageProtocol.__init__(self)

	self.ownjid = ownjid
	self.admin = adminjid

    def connectionMade(self):
	print "[Message] Connected"
	self.send(xmppim.AvailablePresence())

    def connectionLost(self, *args):
	print "[Message] Disconnected %s" % str(args)

    def sendToAdmin(self, body):
	msg = domish.Element((None, 'message'))
	msg['to'] = self.admin.userhost()
	msg['from'] = unicode(self.ownjid)
	msg['type'] = 'chat'
	msg.addElement('body', content=body)

	self.send(msg)

    def onMessage(self, msg):
	print str(msg)

	if msg['type'] == 'chat' and hasattr(msg, 'body'):
	    if jid.JID(msg['from']).userhostJID() != self.admin:
		print "Ignored message from %s" % msg['from']
		return

	    commands = unicode(msg.body).split(u'\n')
	    for command in commands:
		words = command.split()
		if words[0] == 'subscribe':
		    self.pubsub.subscribeMe(words[1])
		elif words[0] == 'unsubscribe':
		    self.pubsub.unsubscribeMe(words[1])
		elif words[0] == 'echo':
		    self.sendToAdmin('echo: %s' % str(msg.body))


class BotPubsubClient(pubsub.PubSubClient):

    def __init__(self, messageProt, service):
	pubsub.PubSubClient.__init__(self)

	self.messageProt = messageProt
	messageProt.pubsub = self

	self.service = jid.internJID(service)

    @inlineCallbacks
    def subscribeMe(self, nodeId):
	yield self.subscribe(self.service, nodeId, self.messageProt.ownjid)
	self.messageProt.sendToAdmin(u'Subscribed to %s ok' % nodeId)

    @inlineCallbacks
    def unsubscribeMe(self, nodeid):
	yield self.unsubscribe(self.service, nodeId, self.messageProt.ownjid)
	self.messageProt.sendToAdmin(u'Subscribed to %s ok' % nodeId)

    def connectionMade(self):
	print "[Pubsub] Connected"

    def connectionLost(self, *args):
	print "[Pubsub] Disconnected %s" % str(args)

    def itemsReceived(self, event):
	print "[Pubsub] Got items from %s" % event.nodeIdentifier
	message = [u'Got items from %s:\n' % event.nodeIdentifier]
	for item in event.items:
	    message.append(u'   %s\n' % item.toXml())
	self.messageProt.sendToAdmin(''.join(message))

xmppclient = client.XMPPClient(botjid, botpass)
xmppclient.logTraffic = True

messageBot = BotMessageProtocol(botjid, admin)
pubsubBot = BotPubsubClient(messageBot, pubsubService)

messageBot.setHandlerParent(xmppclient)
pubsubBot.setHandlerParent(xmppclient)

application = service.Application('testbot')
xmppclient.setServiceParent(application)

