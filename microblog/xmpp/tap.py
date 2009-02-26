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

from twisted.application import internet, service, strports
from twisted.conch import manhole, manhole_ssh
from twisted.cred import portal, checkers
from twisted.web import server

from idavoll import gateway, tap

from microblog.xmpp import idavoll_xmlrpc

class Options(tap.Options):
    optParameters = [
            ('rpcport', None, '8086', 'XML-RPC port'),
    ]

def getManholeFactory(namespace, **passwords):
    def getManHole(_):
        return manhole.Manhole(namespace)

    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = getManHole
    p = portal.Portal(realm)
    p.registerChecker(
            checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f

def makeService(config):
    s = tap.makeService(config)

    bs = s.getServiceNamed('backend')
    cs = s.getServiceNamed('component')

    # Set up XMLRPC service
    xmlrpc = idavoll_xmlrpc.XMLRPC(bs, config['jid'])
    site = server.Site(xmlrpc)
    w = internet.TCPServer(int(config['rpcport']), site, interface='localhost')
    w.setServiceParent(s)

    # Set up a manhole
    namespace = {'service': s,
                 'component': cs,
                 'backend': bs,
                 'xmlrpc': xmlrpc}

    f = getManholeFactory(namespace, admin='admin!pass')
    manholeService = strports.service('2222', f)
    manholeService.setServiceParent(s)

    return s

