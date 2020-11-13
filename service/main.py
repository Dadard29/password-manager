from flask import Flask
from service.config.config import config

# import the controllers
from service.controllers.database_controller import database_blueprint
from service.controllers.session_controller import session_blueprint

app = Flask(config.app['name'])


def start_app():
    # register controllers
    app.register_blueprint(session_blueprint)
    app.register_blueprint(database_blueprint)

    host = config.app['host']
    port = config.app['port']
    debug = config.DEBUG == "1"
    app.run(host, port, debug)


if __name__ == "__main__":
    start_app()
