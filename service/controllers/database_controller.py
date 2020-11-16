from flask import Blueprint, request

from service.controllers.session_controller import session_blueprint
from service.controllers.utils import check_session_token, created, retrieved, deleted, edited, not_found, internal, \
    update_session_activity
from service.models.entry import Entry
from service.repository.globals import session_global

database_blueprint = Blueprint("database_controller", __name__)


@database_blueprint.route("/database/<group>", methods=['POST', 'GET', 'DELETE'])
@check_session_token(request, session_global)
@update_session_activity(session_global)
def database_group(group):
    if request.method == 'POST':
        try:
            return created(
                session_global.database.decrypted.new_group(group))
        except KeyError as k:
            return internal(k)

    elif request.method == 'GET':
        try:
            return retrieved(
                session_global.database.decrypted.get_group(group)
            )
        except KeyError as k:
            return not_found(k)

    elif request.method == 'DELETE':
        try:
            return deleted(
                session_global.database.decrypted.delete_group(group)
            )
        except KeyError as k:
            return not_found(k)


@database_blueprint.route("/database/<group>/<entry>", methods=['POST', 'GET', 'PUT', 'DELETE'])
@check_session_token(request, session_global)
@update_session_activity(session_global)
def database_entry(group, entry):
    if request.method == 'POST':
        try:
            e = Entry(entry, request.json)
            return created(
                session_global.database.decrypted.new_entry(group, e)
            )
        except KeyError as k:
            return internal(k)

    elif request.method == 'GET':
        try:
            return retrieved(
                session_global.database.decrypted.get_entry(group, entry)
            )
        except KeyError as k:
            return not_found(k)

    elif request.method == 'PUT':
        try:
            e = Entry(entry, request.json)
            return edited(
                session_global.database.decrypted.edit_entry(group, e)
            )
        except KeyError as k:
            return not_found(k)

    elif request.method == 'DELETE':
        try:
            return deleted(
                session_global.database.decrypted.delete_entry(group, entry)
            )
        except KeyError as k:
            return not_found(k)
