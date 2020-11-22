from flask import Blueprint, request

from controllers.utils import created, bad_request, retrieved, deleted, check_session_token, internal
from repository.globals import session_global

session_blueprint = Blueprint("session_controller", __name__)


# opens a new session
@session_blueprint.route("/session", methods=['POST'])
def session_post():
    try:
        if session_global.is_active:
            return bad_request("a session is already active")

        # the key (base64 encoded) to use for database encryption/decryption
        master_key = request.headers.get('key')

        session_global.open(master_key)

        return created({
            "token": session_global.token,
            "session": session_global.to_dict()
        })
    except TypeError as te:
        return internal(te)
    except UnicodeDecodeError:
        return internal("failed to open session, decryption failed")


# close the existing session
@session_blueprint.route("/session", methods=['DELETE'])
@check_session_token(request, session_global)
def session_delete():
    # copy current session to return
    d = session_global.to_dict()
    d['is_active'] = False

    session_global.close_manually()

    return deleted(d, "session closed")


# get the existing active session (does not gives the token)
@session_blueprint.route("/session", methods=['GET'])
@check_session_token(request, session_global)
def session_get():
    return retrieved(session_global.to_dict(), "session retrieved")
