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
import os
import sys

import MySQLdb
import jinja2
import webapp2
from webapp2_extras import sessions

from rosefire import RosefireTokenVerifier
from models import Section
from models import Schedule


# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db='dbo')

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db='dbo')

    return db

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
        try:
            db = connect_to_cloudsql()
        except:
            print "Database connection error"
        template = JINJA_ENV.get_template("templates/index.html")
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
    def post(self):
        classInputs = []
        classInputs.append(self.request.get('classOne'))
        classInputs.append(self.request.get('classTwo'))
        classInputs.append(self.request.get('classThree'))
        classInputs.append(self.request.get('classFour'))
        classInputs.append(self.request.get('classFive'))
        classInputs.append(self.request.get('classSix'))
        
        allowedPeriods = self.request.get_all('periodOptions')
        weekendWeds = self.request.get('wednesdayRadio')
        profRating = self.request.get('profRating')
          
        allowedWeds = 1;  
        if weekendWeds == "1":
            allowedWeds = 0;    
        else:
            allowedWeds = 1; 
       
        i = 0
        for period in allowedPeriods:
            allowedPeriods[i] = int(period)
            i = i+1
           
        schedules = []
        schedule = []
        result = []
        try:
            db = connect_to_cloudsql()
        except:
            print "Database connection error"
        sql = "SELECT * FROM Section WHERE Section.CourseNum"
        classes = []
        try:
            for courseNum in classInputs:
                if len(courseNum) > 2:
                    print courseNum
                    cursor = db.cursor()
                    args = (courseNum, allowedWeds, profRating)
                    cursor.callproc('classQuery', args)
                    classOpts = cursor.fetchall()
                    cursor.close()
                    
                    sections = []
                    for row in classOpts:
                        cursor = db.cursor()
                        sql = "SELECT CourseName, CreditHours FROM Class WHERE CourseNum = '" + row[1] + "'"
                        cursor.execute(sql)
                        courseName = cursor.fetchone()
                        cursor.close()
                        section = Section(row[0], row[1], getPeriods(row), row[3], getDays(row), courseName[1], courseName[0])
                        sections.append(section)
                    classes.append(sections)
                
            schedule = findScheduleB(classes, allowedPeriods, weekendWeds)
            args = []
            user_info = json.loads(self.session["user_info"])
            print user_info["username"]
            args.append(str(user_info["username"]))
            for section in schedule.classes:
                args.append(int(section.CRN))
            for x in range(len(args), 7):
                args.append(0)
            cursor = db.cursor()
            cursor.callproc('createFavoritedSchedule', tuple(args)) 
            db.commit() 
            cursor.close()
            
            cursor = db.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            scheduleID = cursor.fetchone()
            schedule.id = scheduleID[0]
            schedules.append(schedule)    
        except:
            print("Unexpected error:", sys.exc_info()[0])
        template = JINJA_ENV.get_template("templates/results.html")
        self.response.out.write(template.render({"user_info": self.session["user_info"], "schedules": schedules}))
     
def getPeriods(row):
    if '-' not in str(row[2]):
        return [int(row[2])]
    periods = str(row[2]).split("-")
    i = 0
    for num in periods:
        periods[i] = int(num)
        i = i + 1
    if len(periods) > 1:
        diff = periods[1] - periods[0]
        start = periods[0]
        periods = []
        for x in range (0, diff + 1):
            periods.append(start + x)
    return periods
        
def getDays(row):
    days = list(row[4]) 
    return days

def findSchedule(classes):
    added = []
    schedule = Schedule()
    for aClass in classes:
        added.append("no")
    i = 0
    for aClass in classes:
        for aSection in aClass:
            if schedule.addClass(aSection) == 1:
                print aSection
                added[i] = 'yes'
                i = i + 1
                break
    for x in added:
        if x is not 'yes':
            print 'not all classes added'
            return -1
    
    return schedule

def findScheduleB(classes, allowedPeriods, weekendWeds):
    added = []
    schedule = Schedule()
    for aClass in classes:
        added.append("no")
    i = 0
    print weekendWeds
    for aClass in classes:
        for aSection in aClass:
            print aSection.days
            if set(aSection.periods) < set(allowedPeriods):
                if weekendWeds == 0 or not (set('W') < set(aSection.days)):
                    if schedule.addClass(aSection) == 1:
                        print aSection
                        added[i] = 'yes'
                        i = i + 1
                        break
    for x in added:
        if x is not 'yes':
            print 'not all classes added'
            return -1
    
    return schedule     
                
        
class FavoritesHandler(BaseHandler):
    def get(self):
        schedules = []
        try:
            db = connect_to_cloudsql()
            cursor = db.cursor()
            user_info = json.loads(self.session["user_info"])
            cursor.callproc('getFavoritedSchedule', [user_info["username"]])
            schedulez = cursor.fetchall()
            cursor.close()
            for schedule in schedulez:
                cursor = db.cursor()
                cursor.callproc('getClassList', [schedule[0]])
                CRNs = cursor.fetchall()
                cursor.close()
                classes = []
                for CRN in CRNs:
                    cursor = db.cursor()
                    sql = "SELECT * FROM Section WHERE CRN = " + str(CRN[1])
                    cursor.execute(sql)
                    aClass = cursor.fetchone()
                    cursor.close()
                    cursor = db.cursor()
                    sql = "SELECT CourseName, CreditHours FROM Class WHERE CourseNum = '" + aClass[1] + "'"
                    cursor.execute(sql)
                    courseName = cursor.fetchone()
                    cursor.close()
                    section = Section(aClass[0], aClass[1], getPeriods(aClass), aClass[3], getDays(aClass), courseName[1], courseName[0])
                    classes.append([section])
                sched = findSchedule(classes)
                sched.id = schedule[0]
                schedules.append(sched)
                print schedules
        except:
            print("Unexpected error:", sys.exc_info()[0])
        template = JINJA_ENV.get_template("templates/favorites.html")
        self.response.out.write(template.render({"user_info": self.session["user_info"], "schedules": schedules}))

class FavoriteAction(BaseHandler):  
    def post(self):    
        try:
            schedule = self.request.get('entity')
            db = connect_to_cloudsql()
            cursor = db.cursor()
            user_info = json.loads(self.session["user_info"])
            args = [user_info["username"], schedule]
            cursor.callproc('favoriteSchedule', args)  
            db.commit()
            cursor.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
        self.redirect('/favorites')
        
class DeleteAction(BaseHandler):
    def post(self):
        try:
            schedule = self.request.get('entity')
            db = connect_to_cloudsql()
            cursor = db.cursor()
            print schedule
            user_info = json.loads(self.session["user_info"])
            args = [user_info["username"], schedule]
            cursor.callproc('deleteSchedule', args)  
            db.commit()
            cursor.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
        self.redirect('/favorites')


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
    ('/favorites', FavoritesHandler),
    ('/favschedule', FavoriteAction),
    ('/delschedule', DeleteAction),
], config=config, debug=True)
