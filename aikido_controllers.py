#
# hub.py
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

import cgi,logging
import datetime,os
import wsgiref.handlers,operator
import base_models,aikido_models

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AikidoMainPage(webapp.RequestHandler):

    def get(self):
        aikido_log = aikido_models.AikidoLog.all()
        dojos = aikido_models.Dojo.all().order('name')
        template_values = {'aikido_log':aikido_log,
                           'dojos':dojos}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/aikido.html')
        self.response.out.write(template.render(path,template_values))

class AikidoAddLogPage(webapp.RequestHandler):

    def get(self):
        dojos = aikido_models.Dojo.all().order('name')
        template_values = {
            'all_dojos':dojos,
            'mode':'add'}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/aikido_log_crud.html')
        self.response.out.write(template.render(path,template_values))        

class DojoAddPage(webapp.RequestHandler):

    def get(self):
        instructors = aikido_models.Sensei.all().order('last')
        styles = aikido_models.AikidoOrganizations.style.choices
        template_values = {'instructors':instructors,
                           'aikido_styles':styles,
                           'mode':'add'}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/dojo_crud.html')
        self.response.out.write(template.render(path,template_values))

class DojoSavePage(webapp.RequestHandler):

    def post(self):
        created_by = users.get_current_user()
        mode = self.request.get('mode')
        dojo_name = self.request.get('dojo_name')
        url = self.request.get('url')
        aikido_org = self.request.get('is_aikido_org')
        place_info = cgi.escape(self.request.get('dojo_addr'))
        location = db.PostalAddress(place_info)
        instructors = self.request.get('dojo_sensei',allow_multiple=True)
        affiliations = self.request.get('affiliations',allow_multiple=True)
        style = self.request.get('style')
        if mode == 'add':
            # Checks to see if Dojo already exists in datastore
            #! Needs to be implemented
            if aikido_org:
                new_dojo = aikido_models.AikidoOrganizations(created_by=created_by,
                                                             name=dojo_name,
                                                             location=location)
            else:
                new_dojo = aikido_models.Dojo(created_by=created_by,
                                              name=dojo_name,
                                              location=location)
            if instructors:
                for teacher in instructors:
                    new_dojo.instructors.append(db.Key(teacher))
            if affiliations:
                for org_key in affiliations:
                    new_dojo.affiliations.append(db.Key(org_key))
            if url:
                new_dojo.url = url
            if style != 'none':
                new_dojo.style = style
            new_dojo.put()
            msg = "%s located at %s added to Spimemanger key=%s" % (new_dojo.name,
                                                                    new_dojo.location,
                                                                    str(new_dojo.key()))
        template_values = {
            'message':msg}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/message.html')
        self.response.out.write(template.render(path,template_values))

class SenseiAddPage(webapp.RequestHandler):

    def get(self):
        dojos = aikido_models.Dojo.all().order('name')
        orgs = aikido_models.AikidoOrganizations.all().order('name')
        template_values = {'mode':'add',
                           'aikido_orgs':orgs,
                           'dojos':dojos}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/sensei_crud.html')
        self.response.out.write(template.render(path,template_values))

class SenseiSavePage(webapp.RequestHandler):
    
    def post(self):
        created_by = users.get_current_user()
        title = self.request.get('title')
        first_name = self.request.get('fir_name')
        middle_name = self.request.get('mid_name')
        last_name = self.request.get('las_name')
        rank = self.request.get('rank')
        dojos = self.request.get('sensei_dojos',allow_multiple=True)
        affiliations = self.request.get('sensei_affiliations',allow_multiple=True)
        sensei_exist_gql = db.GqlQuery('''SELECT * FROM Sensei WHERE
                                          first=:1 AND last=:2''',
                                       first_name,
                                       last_name)
        sensei_exists = sensei_exist_gql.get()
        if sensei_exists:
            msg = '''Instructor %s %s already exists in datastore with
                      key=%s''' % (first_name,
                                   last_name,
                                   sensei_exists.key())
        else:
            new_sensei = aikido_models.Sensei(created_by=created_by,
                                              first=first_name,
                                              last=last_name,
                                              rank=rank)
            if title:
                new_sensei.title = title
            if middle_name:
                new_sensei.middle = middle_name
            for dojo in dojos:
                new_sensei.dojos.append(db.Key(dojo))
            for org in affiliations:
                new_sensei.affiliations.append(db.Key(org))
            sensei_key = new_sensei.put()
            msg = '''New instructor %s %s %s added to datastore,
                     key=%s''' % (new_sensei.title,
                                  new_sensei.first,
                                  new_sensei.last,
                                  new_sensei.key())
        template_values = {'message':msg}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/message.html')
        self.response.out.write(template.render(path,template_values))
        
class TechniqueAddPage(webapp.RequestHandler):

    def get(self):
        attack_query = aikido_models.AikidoTechnique.gql('''WHERE  type_of IN :1
                                                            ORDER BY english_translation''',
                                                         ['kick','strike','grab'])
        all_attacks = attack_query.fetch(1000)
        all_techniques = aikido_models.AikidoTechnique.all().order("english_translation")
        template_values = {
            'all_attacks':all_attacks,
            'technique_types':aikido_models.AikidoTechnique.type_of.choices,
            'start_positions':aikido_models.AikidoTechnique.start_location.choices,
            'end_positions':aikido_models.AikidoTechnique.end_location.choices,
            'all_techniques':all_techniques,
            'mode':'add'}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/techniques_crud.html')
        self.response.out.write(template.render(path,template_values))

class TechniqueSavePage(webapp.RequestHandler):

    def post(self):
        created_by = users.get_current_user()
        if not created_by:
            raise RuntimeError("Must be logged in to save technique")
        mode = self.request.get('mode')
        attack_key = self.request.get('attack')
        eng_trans = self.request.get('eng_name')
        japanese = self.request.get('jap_name')
        type_of_tech = self.request.get('type_of')
        start_location = self.request.get('start_location')
        end_location = self.request.get('end_location')
        variation_key = self.request.get('variation')
        comment = self.request.get('comment')
        # Check datastore for eng_trans or japanese
        if mode == 'add':
            eng_query = db.GqlQuery('''SELECT * FROM AikidoTechnique
                                       WHERE english_translation=:1 AND
                                       japanese=:2''',
                                    eng_trans,
                                    japanese)
            already_exists = eng_query.get()
            if already_exists:
                msg = '''Technique %s (%s) already exists in datastore
                      ''' % (eng_trans,japanese)
            else:
                new_technique = aikido_models.AikidoTechnique(created_by=created_by,
                                                              english_translation=eng_trans,
                                                              type_of=type_of_tech)
                if start_location != 'none':
                    new_technique.start_location = start_location
                else:
                    start_location = ''
                if end_location != 'none':
                    new_technique.end_location = end_location
                else:
                    end_location = ''
                if japanese:
                    new_technique.japanese = japanese
                if attack_key != 'none':
                    attack = db.get(db.Key(attack_key))
                    new_technique.attack = db.get(db.Key(attack_key))
                    attack_name = attack.english_translation
                else:
                    attack_name = ''
                if variation_key != 'none':
                    new_technique.variation_of = db.get(db.Key(variation_key))
                if comment:
                    comment_entity = base_models.Comment(created_by=created_by,
                                                         note=comment)
                    comment_entity.put()
                    new_technique.comment.append(comment_entity.key())
                new_key = new_technique.put()
                msg = '''Technique %s %s %s %s (%s) added to
                         datastore with key=%s''' % (start_location,
                                                     attack_name,
                                                     eng_trans,
                                                     end_location,
                                                     japanese,
                                                     new_key)
        template_values = {
            'message':msg}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/message.html')
        self.response.out.write(template.render(path,template_values))


class Aikido3DMainPage(webapp.RequestHandler):

    def get(self):
        template_values = {
            'message':'Aikido 3D Main Page'}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/aikido3D_base.html')
        self.response.out.write(template.render(path,template_values))

class AikidoPrimitiveShapesPage(webapp.RequestHandler):

    def get(self):
        shape = self.request.get('shape')
        if not shape:
            raise RuntimeError("Page requires shape")
        if shape == 'cube':
            path = os.path.join(os.path.dirname(__file__),
                                'templates/simple.html')
            template_values = {
                'shape':'cube'}
        else:
            raise RuntimeError("Unknown shape %s " % shape)
        self.response.out.write(template.render(path,template_values))
