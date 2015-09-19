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
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import logging
import json
import urllib
from operator import eq
from collections import OrderedDict
import random

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Like(ndb.Model):
    title = ndb.StringProperty(required = True)
    artist = ndb.StringProperty(required = True)
    album = ndb.StringProperty(required = True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

#consumer key = xcBFVugoUDNSh-YdI69i7A

class ResultsHandler(webapp2.RequestHandler):
    def post(self):
        result_template = jinja_environment.get_template('templates/results.html')
        rand_num = random.randint(0,5)
        base_term = "http://api.giphy.com/v1/gifs/search?q="
        user_input = self.request.get("search")
        api_key_url = "&api_key=dc6zaTOxFJmzC&limit=10"
        giphy_data_source = urlfetch.fetch(base_term + user_input + api_key_url)
        logging.info(base_term + user_input + api_key_url)
        giphy_json_content = giphy_data_source.content
        parsed_giphy_dictionary = json.loads(giphy_json_content)
        gif_url= parsed_giphy_dictionary['data'][rand_num]['images']['original']['url']

        template_titles = {}
        template_artists = {}
        template_albums = {}
        search_results = []
        user_search = self.request.get('search')

        term = {'term' : user_search}
        search_term = urllib.urlencode(term)
        base_url = 'https://itunes.apple.com/search?media=music&'
        search_url = base_url + search_term
        url_content = urlfetch.fetch(search_url).content
        parsed_url_dictionary = json.loads(url_content)

        for index, key in enumerate(parsed_url_dictionary['results']):
            search_name = parsed_url_dictionary['results'][index]['trackName']
            template_titles.update({'key' + str(index) : search_name})

        for index, key in enumerate(parsed_url_dictionary['results']):
            search_artist = parsed_url_dictionary['results'][index]['artistName']
            template_artists.update({'key' + str(index) : search_artist})

        for index, key in enumerate(parsed_url_dictionary['results']):
            if 'collectionName' in parsed_url_dictionary['results'][index].keys():
                search_album = parsed_url_dictionary['results'][index]['collectionName']
                template_albums.update({'key' + str(index) : search_album})
            else:
                template_albums.update({'key' + str(index) : ''})

        for key, value in template_titles.iteritems():
            title = value
            artist = template_artists[key]
            album = template_albums[key]
            current_search_result = Like(title = title, artist = artist, album = album)
            search_results.append(current_search_result)

        passed_vars = {'gif1': gif_url,
                       'songs': template_titles,
                       'artists': template_artists,
                       'albums': template_albums,
                       'searches': search_results}

        self.response.out.write(result_template.render(passed_vars))

class SadHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/sad.html')
        self.response.write(template.render())

class HappyHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/happy.html')
        self.response.write(template.render())

class SurprisedHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/surprised.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/sad', SadHandler),
    ('/happy', HappyHandler),
    ('/surprised', SurprisedHandler)
], debug=True)
