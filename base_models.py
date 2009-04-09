#
# base_models.py
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
# Copyright 2009 Jeremy Nelson
#

# Import statements
import cgi,logging
import datetime,os

from google.appengine.ext import db
from google.appengine.api import users

class Base(db.Model):
    '''Base data model class, used for other classes in app'''
    created_by = db.UserProperty()
    created_on = db.DateTimeProperty(auto_now_add=True)
    tags = db.ListProperty(db.Category)

class Dojo(Base):
    '''Dojo is an organization that supports training in
       a martial art'''
    name = db.StringProperty(required=True)
    location = db.PostalAddressProperty()
    instructors = db.ListProperty(db.Key)

class AikidoLog(Base):
    ''' Tracks Aikido Practice '''
    class_datetime = db.DateTimeProperty(required=True)
    comments = db.ListProperty(db.Key)
    dojo = db.ReferenceProperty(Dojo)
    instructors = db.ListProperty(db.Key)
    location = db.PostalAddressProperty()
    participants = db.ListProperty(db.Key)
    techniques = db.ListProperty(db.Key)
    total_minutes = db.IntegerProperty()

    def get_instructors(self):
        instructors = list()
        for key in self.instructors:
            person = db.get(key)
            instructors.append(person.full_name)
        instructors.sort()
        return instructors

class AikidoTechnique(Base):
    ''' Listing of Aikido Techniques '''
    attack = db.SelfReferenceProperty(collection_name="attack_technique")
    comments = db.ListProperty(db.Key)
    english_translation = db.StringProperty(required=True)
    end_location = db.StringProperty(required=False,
                                     choices=(['omote',
                                               'ura',
                                               'none']))
    japanese = db.StringProperty()
    sources = db.ListProperty(db.Key)
    type_of = db.StringProperty(required=True,
                                choices=(['drop',
                                          'grab',
                                          'exercise',
                                          'henkawaza',
                                          'kick',
                                          'kokyuho',
                                          'pin',
                                          'strike',
                                          'throw']))
    variation_of = db.SelfReferenceProperty()
    
class Comment(Base):
    '''Stores notes about other data models in app'''
    note = db.TextProperty()

class Person(Base):
    '''Stores info about a person'''
    first = db.StringProperty(required=False)
    last = db.StringProperty(required=True)
    rank = db.StringProperty()
    title = db.StringProperty()

    def full_name(self):
        full_name = str()
        if self.title:
            full_name += "%s " % self.title
        if self.first:
            full_name += "%s " % self.first
        if self.last:
            full_name += "%s " % self.last
        return full_name
            
    
class Project(Base):
    '''Project class stores information about a projects'''
    name = db.StringProperty(required=True)
    start = db.DateProperty()
    end = db.DateProperty()
    budget = db.FloatProperty()
    comments = db.ListProperty(db.Key)
    members = db.ListProperty(users.User)
    status = db.StringProperty(required=True,
                               choices=(['proposed',
                                         'in-progress',
                                         'completed',
                                         'abandoned']))
    url = db.LinkProperty(required=False)

    def check_range(self):
        if start > end:
            raise ValueError("Project start date cannot start before end date")

class SocialNetwork(Base):
    base_url = db.LinkProperty(required=True)
    name = db.StringProperty(required=True)
    user_name = db.StringProperty()
    user_url = db.LinkProperty()
    
