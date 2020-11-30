from flask import Flask

from gui.webapp import webapp

templates_dir = "clients/gui/templates"
static_dir = "clients/gui/static"
app = Flask("password-manager-gui", template_folder=templates_dir, static_folder=static_dir)

app.register_blueprint(webapp)

app.run("localhost", "8080")
