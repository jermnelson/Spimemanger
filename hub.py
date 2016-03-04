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

        
#application = webapp.WSGIApplication([
#    ('/',HubPage),
#    ('/aikido/',aikido_controllers.AikidoMainPage),
#    ('/aikido/dojos/add',aikido_controllers.DojoAddPage),
#    ('/aikido/dojos/save',aikido_controllers.DojoSavePage),
#    ('/aikido/logs/add',aikido_controllers.AikidoAddLogPage),
#    ('/aikido/sensei/add',aikido_controllers.SenseiAddPage),
#    ('/aikido/sensei/save',aikido_controllers.SenseiSavePage),
#    ('/aikido/techniques/add',aikido_controllers.TechniqueAddPage),
#    ('/aikido/techniques/save',aikido_controllers.TechniqueSavePage),
#    ('/aikido/3D/',aikido_controllers.Aikido3DMainPage),
#    ('/aikido/3D/primitives',aikido_controllers.AikidoPrimitiveShapesPage),
#    ('/elibrary/',HubPage),
#    ], debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hub():
    return render_template("hub.html")

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()


