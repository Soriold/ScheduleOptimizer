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
import json
import logging
import os

import jinja2
from rosefire import RosefireTokenVerifier
import webapp2
from webapp2_extras import sessions


# This normally shouldn't be checked into Git
ROSEFIRE_SECRET = 'BtVrAIrkLfN163ft4opm'

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True)

# From: https://webapp2.readthedocs.io/en/latest/api/webapp2_extras/sessions.html
class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class MainHandler(BaseHandler):
    def get(self):
        template = JINJA_ENV.get_template("templates/index.html.jinja")
        if "user_info" in self.session:
          user_info = json.loads(self.session["user_info"])
          print("user_info", user_info)
          self.response.out.write(template.render({"user_info": user_info}))
        else:
          self.response.out.write(template.render())

class LoginHandler(BaseHandler):
    def get(self):
        if "user_info" not in self.session:
            token = self.request.get('token')
            auth_data = RosefireTokenVerifier(ROSEFIRE_SECRET).verify(token)
            user_info = {"name": auth_data.name,
                         "username": auth_data.username,
                         "email": auth_data.email,
                         "role": auth_data.group}
            self.session["user_info"] = json.dumps(user_info)
        self.redirect(uri="/")

class LogoutHandler(BaseHandler):
    def get(self):
        del self.session["user_info"]
        self.redirect(uri="/")

config = {}
config['webapp2_extras.sessions'] = {
    # This key is used to encrypt your sessions
    'secret_key': 'BtVrAIrkLfN163ft4opm',
}

class ResultHandler(BaseHandler):
    def get(self):
        template = JINJA_ENV.get_template("templates/results.html.jinja")
        self.response.out.write(template.render({"user_info": self.session["user_info"]}))
        
class FavoritesHandler(BaseHandler):
    def get(self):
        template = JINJA_ENV.get_template("templates/favorites.html.jinja")
        self.response.out.write(template.render({"user_info": self.session["user_info"]}))

config = {}
config['webapp2_extras.sessions'] = {
    # This key is used to encrypt your sessions
    'secret_key': 'BtVrAIrkLfN163ft4opm',
}

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/results', ResultHandler),
    ('/favorites', FavoritesHandler)
], config=config, debug=True)
