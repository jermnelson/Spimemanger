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
import base_models

from google.appengine.ext import db
from google.appengine.api import users

class Dojo(base_models.Base):
    '''Dojo is an organization that supports training in
       a martial art'''
    name = db.StringProperty(required=True)
    url = db.LinkProperty()
    location = db.PostalAddressProperty()
    instructors = db.ListProperty(db.Key)
    affiliations = db.ListProperty(db.Key)

class AikidoLog(base_models.Base):
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

class AikidoTechnique(base_models.Base):
    ''' Listing of Aikido Techniques '''
    attack = db.SelfReferenceProperty(collection_name="attack_technique")
    comments = db.ListProperty(db.Key)
    english_translation = db.StringProperty(required=True)
    start_location = db.StringProperty(required=False,
                                       choices=(['hanmi handachi',
                                                 'henka waza',
                                                 'none',
                                                 'suwaru',
                                                 'ushiro']))
                                                 
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

class AikidoOrganizations(Dojo):
    ''' Usually an umbrella group that has dojo affiliation and
        represent a particular style of Aikido '''
    style = db.StringProperty(required=False,
                              choices=(['aikikai',
                                        'iwama',
                                        'kata no nai'
                                        'ki no kenkyu kai',
                                        'tomiki',
                                        'yoseikan',
                                        'yoshinkan']))


class Sensei(base_models.Person):
    ''' Extended person to include affliation and Martial Art
        Ranking '''
    rank = db.StringProperty()
    dojos = db.ListProperty(db.Key)
    affiliations = db.ListProperty(db.Key)
