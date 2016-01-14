# -*- coding: utf-8 -*-

"""Unittests for flask.
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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

from gevent import monkey
monkey.patch_all()

import sys, os
import time, datetime
import unittest
import urllib
import urllib2

from flask_bower import Bower
from flask_cache import Cache

from janitoo_nosetests import JNTTBase

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine
from janitoo_db.migrate import Config as alConfig, collect_configs, janitoo_config

class JNTTFlask(JNTTBase):
    """Test the flask
    """
    flask_conf = "tests/data/janitoo_flask.conf"

    def setUp(self):
        JNTTBase.setUp(self)
        self.app = self.create_app()
        self.client = self.app.test_client()
        # We need to create a context in order for extensions to catch up
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        if getattr(self, '_ctx', None) is not None:
            self._ctx.pop()
            del self._ctx
        self.client = None
        self.app = None
        JNTTBase.tearDown(self)

    def assertUrl(self, url='/', code="200 OK"):
        response = self.client.get(url)
        print response
        self.assertEquals(response.status, code)

    def assertEndpoint(self, endpoint='static'):
        self.assertTrue('static' in self.get_routes())

    def get_routes(self):
        res = {}
        for rule in self.app.url_map.iter_rules():
            res["{}".format(rule.endpoint)] = {'methods':rule.methods, 'rule':"{}".format(rule)}
        return res

    def list_routes(self):
        output = []
        routes = self.get_routes()
        for route in routes:
            line = urllib.unquote("{:50s} {:30s} {}".format(route, routes[route]['methods'], routes[route]['rule']))
            output.append(line)
        for line in sorted(output):
            print(line)

class JNTTFlaskCommon():
    """Common tests for flask
    """

    def test_001_app_is_loaded(self):
        self.assertEqual(type(self.app.extensions['cache']), type(Cache()))
        self.assertEqual(type(self.app.extensions['bower']), type(Bower()))
        print self.get_routes()
        self.assertEndpoint('bower.serve')
        self.assertEndpoint('static')

    def test_011_home_is_up(self):
        self.list_routes()
        self.assertUrl('/', "200 OK")

