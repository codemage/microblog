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

class BotPresenceProtocol(xmppim.PresenceClientProtocol):
    def subscribeReceived(self, entity): # auto-approve subcription requests
	self.subscribed(entity)

class BotRosterProtocol(xmppim.RosterClientProtocol):
    pass

class BotMessageProtocol(xmppim.MessageProtocol):
    def __init__(self, ownjid, presenceProt, rosterProt):
	xmppim.MessageProtocol.__init__(self)

	self.ownjid = ownjid
	self.presenceProt = presenceProt
	self.rosterProt = rosterProt

    @inlineCallbacks
    def connectionInitialized(self):
	print "[MessageBot] Connected %s" % self.ownjid
	
	self.roster = yield self.rosterProt.getRoster()
	self.send(xmppim.AvailablePresence())

    def connectionLost(self, *args):
	print "[MessageBot] Disconnected %s" % str(args)

    def sendMessage(self, to, body):
	msg = domish.Element((None, 'message'))
	msg['to'] = to
	msg['from'] = unicode(self.ownjid)
	msg['type'] = 'chat'
	msg.addElement('body', content=body)

	self.send(msg)

def getBot(botjid, botpass, logTraffic):
    botjid = jid.internJID(botjid)

    xmppclient = client.XMPPClient(botjid, botpass)
    xmppclient.logTraffic = logTraffic

    presenceProt = BotPresenceProtocol()
    presenceProt.setHandlerParent(xmppclient)
    rosterProt = BotRosterProtocol()
    rosterProt.setHandlerParent(xmppclient)
    messageBot = BotMessageProtocol(botjid, presenceProt, rosterProt)
    messageBot.setHandlerParent(xmppclient)
    BotPresenceProtocol().setHandlerParent(xmppclient)

    return xmppclient, messageBot

