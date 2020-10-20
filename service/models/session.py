import sched
import secrets
import time
from datetime import datetime, timedelta


# the session object is used to manage database loading, unloading and access
from flask import current_app


class Session(object):
    # tells if the session is active
    is_active = False

    # the authentication temporary token to used for all data access request
    token = None

    # tells when the session has been created
    created_at = None

    # tells when occurred the last user activity
    last_activity_time = None

    # the duration in seconds before closing the session if no user activity is detected
    timeout = 120

    # the scheduler used to manage the session closing
    scheduler = None

    # the event when the session closing occurs
    closing_event = None

    # the database object
    database = None

    def __init__(self):
        self.is_active = False

        # init the closing scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def to_dict(self):
        return dict(
            is_active=self.is_active,
            created_at=self.created_at,
            last_activity_time=self.last_activity_time,
            timeout=self.timeout
        )

    def open(self, timeout=None):
        self.created_at = datetime.now()
        self.last_activity_time = datetime.now()

        if timeout is not None:
            self.timeout = timeout

        self.is_active = True
        self.token = self._generate_token()

        # schedule automated closing
        self._reschedule_closing()

        current_app.logger.info("session opened")

    def update_activity(self):
        self.last_activity_time = datetime.now()
        self._reschedule_closing()

    def close(self):
        self.is_active = False
        self.token = None
        self.created_at = None
        self.last_activity_time = None
        self.closing_event = None

        # write the database change
        # todo

        # free the database memory
        # todo

        current_app.logger.info("session closed")

    def _reschedule_closing(self):
        if self.closing_event is not None:
            self.scheduler.cancel(self.closing_event)

        closing_time = self.last_activity_time + timedelta(seconds=self.timeout)
        self.closing_event = self.scheduler.enterabs(closing_time.timestamp(), 1, self.close)

    @staticmethod
    def _generate_token():
        return secrets.token_hex(16)
