# responses
from functools import wraps

from models.session import Session

from flask import current_app


def format_body(body, code, message):
    return {
               "code": code,
               "message": message,
               "body": body
           }, code


def format_error(code, message):
    current_app.logger.error(message)
    if not isinstance(message, str):
        message = str(message)
    return {
               "code": code,
               "message": message
           }, code


def created(body, message="object created"):
    code = 201
    return format_body(body, code, message)


def edited(body, message="object edited"):
    code = 200
    return format_body(body, code, message)


def deleted(body, message="object removed"):
    code = 200
    return format_body(body, code, message)


def retrieved(body, message="object retrieved"):
    code = 200
    return format_body(body, code, message)


def bad_request(message="bad request"):
    code = 400
    return format_error(code, message)


def not_found(message="not found"):
    code = 404
    return format_error(code, message)


def internal(message="internal server error"):
    code = 500
    return format_error(code, message)


def unauthorized(message="unauthorized"):
    code = 401
    return format_error(code, message)


# auth

# decorator to check the session at every configured endpoint
def check_session_token(request, session: Session):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not session.is_active:
                return not_found("no active session found")

            token = request.headers.get('Authorization')
            if not token == session.token:
                return unauthorized("wrong token")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def update_session_activity(session: Session):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session.update_activity()

            return func(*args, **kwargs)

        return wrapper

    return decorator
