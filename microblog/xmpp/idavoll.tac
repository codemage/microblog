"""
    TAC for Idavoll for use in microblog app

    Copyright (c) 2009 Walter Mundt

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

from twisted.application import service
from twisted.words.protocols.jabber.jid import JID

from microblog.xmpp import tap

config = {
    'jid': JID('pubsub.lerran.apogean.org'),
    'secret': 'secret',
    'rhost': '127.0.0.1',
    'rport': 5347,
    'backend': 'pgsql',
    'verbose': True,
    'hide-nodes': False,
    'rpcport': 8086,
    'dbuser': 'microblog',
    'dbpass': 'secret',
    'dbname': 'pubsub',
    'dbhost': 'localhost',
    'dbport': 5432
}

application = service.Application("Microblog-pubsub")
idavollService = tap.makeService(config)
idavollService.setServiceParent(application)

