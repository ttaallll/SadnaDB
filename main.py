#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os

import jinja2
import MySQLdb

from myconfig import *
from feeder import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def tryConnectToDb():
    env = os.getenv('SERVER_SOFTWARE')
    if env and env.startswith('Google App Engine/'):
        # Connecting from App Engine
        db = MySQLdb.connect(
            unix_socket='/cloudsql/sadnadb:db1',
            user='root')
    else:
        # You may also assign an IP Address from the access control
        # page and use it to connect from an external network.

        db = MySQLdb.connect(host=DB_IP, user='root')
        pass

    str1 = ''

    cursor = db.cursor()
    cursor.execute('SELECT 1 + 1')
    for r in cursor.fetchall():
        for r2 in r:
            print str(r2)
            str1 += '%s\n' % str(r2)

    db.close()

    return str1


def createDbConnection():
    env = os.getenv('SERVER_SOFTWARE')
    if env and env.startswith('Google App Engine/'):
        # Connecting from App Engine
        db = MySQLdb.connect(
            unix_socket='/cloudsql/sadnadb:db1',
            user='root')
    else:
        # You may also assign an IP Address from the access control
        # page and use it to connect from an external network.

        db = MySQLdb.connect(host=DB_IP, user='root')

    return db


def createRequestContext():
    db1 = createDbConnection()

    return {
        "db": db1
    }


def clearRequestContext(requestContext):

    # close db connection
    requestContext["db"].close()


class UploadFileHandler(webapp2.RequestHandler):
    def post(self):

        file1 = self.request.get('file')

        requestContext = createRequestContext()

        try:
            addBookToDB(requestContext, file1, 'gutenberg')
            requestContext["db"].commit()
        except Exception as e:
            requestContext["db"].rollback()

        clearRequestContext(requestContext)

        self.response.write('123')


class MainHandler(webapp2.RequestHandler):
    def get(self):

        requestContext = createRequestContext()
        lastBook = getLastBookFromDB(requestContext)
        clearRequestContext(requestContext)

        template_values = {
            'user': 1,
            'lastBook': lastBook
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', UploadFileHandler)
], debug=True)
