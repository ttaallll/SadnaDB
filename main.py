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
from google.appengine.api import taskqueue

import jinja2
import MySQLdb

from myconfig import *
from feeder import *
from storage import *
from book import *
from words import *
from group import *

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
        filename1 = self.request.POST['file'].filename

        # upload to cloud
        bookUrl = uploadToStorage(filename1, file1)

        taskqueue.add(url='/addBookTask', params={'bookUrl': bookUrl})

        self.response.write(bookUrl)


class ShowBookHandler(webapp2.RequestHandler):
    def get(self):
        bookId = self.request.get('id')

        requestContext = createRequestContext()

        book = getBookForTemplate(requestContext, bookId)

        clearRequestContext(requestContext)

        template_values = {
            'book': book,
            'bookId': bookId
        }

        template = JINJA_ENVIRONMENT.get_template('book.html')
        self.response.write(template.render(template_values))


class ShowWordHandler(webapp2.RequestHandler):
    def get(self):
        wordId = self.request.get('id')

        bookId = None
        if 'bookId' in self.request.GET:
            bookId = self.request.get('bookId')

        requestContext = createRequestContext()

        word = getWordForTemplate(requestContext, wordId, bookId)

        clearRequestContext(requestContext)

        template_values = {
            'word': word
        }

        template = JINJA_ENVIRONMENT.get_template('word.html')
        self.response.write(template.render(template_values))


class SearchWordInBookHandler(webapp2.RequestHandler):
    def get(self):

        rc = createRequestContext()

        bookId = self.request.get('bookId')

        if 'wordNumber' in self.request.GET and self.request.get('wordNumber') != '':
            wordId = getWordByLocation(rc, bookId, 'wordNumber', self.request.get('wordNumber'))
        elif 'lineNumber' in self.request.GET and self.request.get('lineNumber') != '' and \
             'wordInLine' in self.request.GET and self.request.get('wordInLine') != '':
            wordId = getWordByLocation(rc, bookId, 'wordInLine', (self.request.get('lineNumber'), self.request.get('wordInLine')))
        else:
            self.response.write('bad params to search')
            clearRequestContext(rc)
            return

        clearRequestContext(rc)

        if wordId:
            self.redirect('/word?id=' + str(wordId) + '&bookId=' + bookId)
        else:
            self.redirect('/notFound')


class SearchHandler(webapp2.RequestHandler):
    def get(self):

        rc = createRequestContext()

        results = {}
        searchValue = None

        if 'wordName' in self.request.GET and self.request.get('wordName') != '':
            wordId = getWordByName(rc, self.request.get('wordName'))

            clearRequestContext(rc)

            if wordId:
                self.redirect('/word?id=' + str(wordId))
            else:
                self.redirect('/notFound?x=' + self.request.get('wordName'))
            return

        elif 'title' in self.request.GET and self.request.get('title') != '':
            searchValue = self.request.get('title')
            results['books'] = getBooksByMetadata(rc, 'title', searchValue)
        elif 'author' in self.request.GET and self.request.get('author') != '':
            searchValue = self.request.get('author')
            results['books'] = getBooksByMetadata(rc, 'author', searchValue)
        elif 'releaseDate' in self.request.GET and self.request.get('releaseDate') != '':
            searchValue = self.request.get('releaseDate')
            results['books'] = getBooksByMetadata(rc, 'releaseDate', searchValue)
        elif 'language' in self.request.GET and self.request.get('language') != '':
            searchValue = self.request.get('language')
            results['books'] = getBooksByMetadata(rc, 'language', searchValue)

        clearRequestContext(rc)

        if 'books' in results and len(results['books']) == 0:
            self.redirect('/notFound?x=' + searchValue)
            return

        template_values = {
            'results': results
        }

        template = JINJA_ENVIRONMENT.get_template('searchResults.html')
        self.response.write(template.render(template_values))


class AddBookTaskHandler(webapp2.RequestHandler):
    def post(self):
        bookUrl = self.request.get('bookUrl')

        requestContext = createRequestContext()

        try:
            addBookToDB(requestContext, bookUrl, 'gutenberg')
            requestContext["db"].commit()
        except Exception as e:
            print e
            requestContext["db"].rollback()

        clearRequestContext(requestContext)


class MainHandler(webapp2.RequestHandler):
    def get(self):

        requestContext = createRequestContext()
        lastBooks = getLastNBookFromDB(requestContext, 5)
        clearRequestContext(requestContext)

        template_values = {
            'user': 1,
            'lastBooks': lastBooks
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class NotFoundHandler(webapp2.RequestHandler):
    def get(self):

        template_values = {}
        if 'x' in self.request.GET:
            template_values['x'] = self.request.get('x')

        template = JINJA_ENVIRONMENT.get_template('notFound.html')
        self.response.write(template.render(template_values))


class ShowGroupHandler(webapp2.RequestHandler):
    def get(self):

        groupId = self.request.get('id')

        requestContext = createRequestContext()
        group = getGroup(requestContext, groupId)
        clearRequestContext(requestContext)

        template_values = {
            'group': group
        }

        template = JINJA_ENVIRONMENT.get_template('group.html')
        self.response.write(template.render(template_values))


class CreateGroupHandler(webapp2.RequestHandler):
    def get(self):

        rc = createRequestContext()

        if 'groupName' in self.request.GET and self.request.get('groupName') != '':
            groupId = createGroup(rc, self.request.get('groupName'))
        else:
            self.response.write('no name for group given')
            clearRequestContext(rc)
            return

        clearRequestContext(rc)

        self.redirect('/group?id=' + str(groupId))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', UploadFileHandler),
    ('/addBookTask', AddBookTaskHandler),
    ('/book', ShowBookHandler),
    ('/word', ShowWordHandler),
    ('/search', SearchHandler),
    ('/notFound', NotFoundHandler),
    ('/searchWordInBook', SearchWordInBookHandler),
    ('/createGroup', CreateGroupHandler),
    ('/group', ShowGroupHandler),
], debug=True)
