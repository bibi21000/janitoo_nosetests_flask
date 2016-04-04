# -*- coding: utf-8 -*-

"""Unittests for socketio.
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import sys, os
import time, datetime
import unittest

#~ from flask import Flask, session, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from janitoo_nosetests import JNTTBase

from janitoo.options import JNTOptions


class JNTTSocketIO(JNTTBase):
    """Test the flask
    """
    flask_conf = "tests/data/janitoo_flask.conf"
    namespace = "/janitoo"

    def setUp(self):
        JNTTBase.setUp(self)
        self.app = self.create_app()
        self.socketio = self.app.extensions['socketio']
        # We need to create a context in order for extensions to catch up
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        self.app.extensions['janitoo'].start_listener()
        self.client = None

    def tearDown(self):
        time.sleep(10)
        try:
            self.client.disconnect(self.namespace)
        except RuntimeError:
            pass
        except AttributeError:
            pass
        time.sleep(1)
        self.client = None
        print "Stop"
        try:
            self.app.extensions['janitoo'].stop_listener()
        except RuntimeError:
            pass
        except AttributeError:
            pass
        del self.app.extensions['janitoo']
        try:
            self.app.extensions['socketio'].stop()
        except RuntimeError:
            pass
        except AttributeError:
            pass
        del self.app.extensions['socketio']
        self.app = None
        if getattr(self, '_ctx', None) is not None:
            self._ctx.pop()
            del self._ctx
        JNTTBase.tearDown(self)

    def connect(self):
        time.sleep(1)
        self.client = self.socketio.test_client(self.app, namespace=self.namespace)
        print 'client.sid %s' % self.client.sid
        time.sleep(1)

class JNTTSocketIOCommon():
    """Common tests for flask
    """
    def test_001_server_connect(self):
        self.connect()
        received = self.client.get_received(self.namespace)
        print received
        self.assertTrue(len(received) >= 1)
        #~ self.assertEqual(received[0]['args'], [{'data': 'Connected'}])
