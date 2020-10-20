from flask import request, jsonify, Blueprint


def session_post():
    return dict(action='create session')


def session_delete():
    return dict(action='delete session')


def session_get():
    return dict(action='get session')


session_blueprint = Blueprint("session_controller", __name__)
methods_handlers = {
    "GET": session_get(),
    "POST": session_post(),
    "DELETE": session_delete()
}


@session_blueprint.route("/session", methods=methods_handlers.keys())
def session_controller():
    d = methods_handlers[request.method]
    return jsonify(d)
