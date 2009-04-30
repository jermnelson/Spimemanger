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
import base_models,aikido_controllers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class HubPage(webapp.RequestHandler):

    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        social_networks = base_models.SocialNetwork.all()
        projects = base_models.Project.all()
        
        template_values = {'url':url,
                           'url_linktext':url_linktext,
                           'social_networks':social_networks,
                           'projects':projects}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/hub.html')
        self.response.out.write(template.render(path,template_values))
        
application = webapp.WSGIApplication([
    ('/',HubPage),
    ('/aikido/',aikido_controllers.AikidoMainPage),
    ('/aikido/dojos/add',aikido_controllers.DojoAddPage),
    ('/aikido/dojos/save',aikido_controllers.DojoSavePage),
    ('/aikido/logs/add',aikido_controllers.AikidoAddLogPage),
    ('/aikido/sensei/add',aikido_controllers.SenseiAddPage),
    ('/aikido/sensei/save',aikido_controllers.SenseiSavePage),
    ('/aikido/techniques/add',aikido_controllers.TechniqueAddPage),
    ('/aikido/techniques/save',aikido_controllers.TechniqueSavePage),
    ('/aikido/3D/',aikido_controllers.Aikido3DMainPage),
    ('/aikido/3D/primitives',aikido_controllers.AikidoPrimitiveShapesPage),
    ('/elibrary/',HubPage),
    ], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()


