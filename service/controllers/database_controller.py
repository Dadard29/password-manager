from datetime import datetime

from flask import Blueprint, request

from controllers.utils import check_session_token, created, retrieved, deleted, edited, not_found, internal, \
    update_session_activity, bad_request
from models.entry import Entry, TYPE_ENTRY
from models.utils import get_current_date
from repository.globals import session_global

database_blueprint = Blueprint("database_controller", __name__)


@database_blueprint.route("/database/directory", methods=['POST', 'GET', 'DELETE'])
@check_session_token(request, session_global)
@update_session_activity(session_global)
def database_directories():
    path = request.args['path']
    dir_name = request.args['dir_name']

    if request.method == 'POST':
        try:
            return created(
                session_global.database.decrypted.new_directory(path, dir_name)
            )
        except KeyError as k:
            return internal(k)

    elif request.method == 'GET':
        try:
            return retrieved(
                session_global.database.decrypted.get_directory(path, dir_name)
            )
        except KeyError as k:
            return not_found(k)
        except TypeError as te:
            return internal(te)

    elif request.method == 'DELETE':
        try:
            return deleted(
                session_global.database.decrypted.delete_directory(path, dir_name)
            )
        except KeyError as k:
            return not_found(k)
        except TypeError as te:
            return internal(te)


@database_blueprint.route("/database/entry", methods=['POST', 'GET', 'PUT', 'DELETE'])
@check_session_token(request, session_global)
@update_session_activity(session_global)
def database_entry():
    path = request.args['path']
    entry_name = request.args['entry_name']

    if request.method == 'POST':
        try:
            e = Entry(entry_name, dict(
                type=TYPE_ENTRY,
                created_at=get_current_date(),
                updated_at=get_current_date(),
                content=request.json
            ))
            return created(
                session_global.database.decrypted.new_entry(path, e)
            )
        except KeyError as k:
            return internal(k)

    elif request.method == 'GET':
        try:
            return retrieved(
                session_global.database.decrypted.get_entry(path, entry_name)
            )
        except KeyError as k:
            return not_found(k)
        except TypeError as te:
            return internal(te)

    elif request.method == 'PUT':
        try:
            return edited(
                session_global.database.decrypted.update_entry(
                    path, entry_name, request.json
                )
            )
        except KeyError as k:
            return not_found(k)

    elif request.method == 'DELETE':
        try:
            return deleted(
                session_global.database.decrypted.delete_entry(path, entry_name)
            )
        except KeyError as k:
            return not_found(k)
        except TypeError as te:
            return internal(te)
