import sched
import secrets
import threading
import time
from datetime import datetime, timedelta


# the session object is used to manage database loading, unloading and access
from os import environ

from flask import current_app

from config.config import config
from models.database import Database


class Session(object):
    # -- DEFAULT VALUES AT INITIALIZATION -- #

    # tells if the session is active
    is_active = False

    # the authentication temporary token to used for all data access request
    token = None

    # tells when the session has been created
    created_at = None

    # tells when occurred the last user activity
    last_activity_time = None

    # the duration in seconds before closing the session if no user activity is detected
    timeout = config.session['timeout']

    # the database object
    database = None

    # the scheduler
    scheduler = sched.scheduler()
    closing_event = None
    last_active_session = datetime.now()

    def __init__(self):
        # open the db
        file_path = config.DB_PATH
        self.database = Database(file_path)

    def to_dict(self):
        return dict(
            is_active=self.is_active,
            created_at=self.created_at,
            last_activity_time=self.last_activity_time,
            timeout=self.timeout
        )

    def open(self, master_key):

        self.database.load(master_key)

        self.created_at = datetime.now()
        self.last_activity_time = datetime.now()

        self.is_active = True
        self.token = self._generate_token()

        # schedule automated closing
        self._reschedule_closing()

        current_app.logger.info("session opened")

    def update_activity(self):
        self.last_activity_time = datetime.now()
        self._reschedule_closing()

    def close(self):
        # reset to default values
        self.is_active = False
        self.token = None
        self.created_at = None
        self.last_activity_time = None

        # write the database change
        self.database.save()
        self.database.unload()

        # cant use app logger cuz can be called in multi threaded context
        print(f" {str(datetime.now())}: session closed")

        self.closing_event = None
        self.last_active_session = datetime.now()

    def _reschedule_closing(self):
        current_app.logger.info('rescheduled session closing')
        if self.closing_event is not None:
            self.scheduler.cancel(self.closing_event)

        self.closing_event = self.scheduler.enter(self.timeout, 1, self.close)
        t = threading.Thread(target=self.scheduler.run)
        t.start()
        return

    @staticmethod
    def _generate_token():
        if config.DEBUG == "1":
            return "session_token"

        return secrets.token_hex(16)
