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

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

#consumer key = xcBFVugoUDNSh-YdI69i7A

class ResultsHandler(webapp2.RequestHandler):
    def post(self):
        result_template = jinja_environment.get_template('templates/results.html')
        base_term = "http://api.giphy.com/v1/gifs/search?q="
        user_input = self.request.get("search")
        api_key_url = "&api_key=dc6zaTOxFJmzC&limit=10"
        giphy_data_source = urlfetch.fetch(base_term + user_input + api_key_url)
        logging.info(base_term + user_input + api_key_url)
        giphy_json_content = giphy_data_source.content
        parsed_giphy_dictionary = json.loads(giphy_json_content)
        gif_url= parsed_giphy_dictionary['data'][0]['images']['original']['url']
        template_vars = {"gif1": gif_url}
        self.response.out.write(result_template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler)
], debug=True)
