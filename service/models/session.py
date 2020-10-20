import sched
import time
from datetime import datetime, timedelta


# the session object is used to manage database loading, unloading and access
class Session(object):
    # tells if the session is active
    is_active = False

    # the authentication temporary token to used for all data access request
    token = None

    # tells when occurred the last user activity
    last_activity_time = datetime.now()

    # the duration in seconds before closing the session if no user activity is detected
    timeout = 120

    # the scheduler used to manage the session closing
    scheduler = None

    # the event when the session closing occurs
    closing_event = None

    # the database object
    # fixme

    def __init__(self):
        self.is_active = False

    def open(self, timeout=120):
        self.last_activity_time = datetime.now()
        self.timeout = timeout
        self.is_active = True
        self.token = self._generate_token()

        # init the closing scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self._reschedule_closing()

    def update_activity(self):
        self.last_activity_time = datetime.now()
        self._reschedule_closing()

    def close(self):
        self.is_active = False
        self.token = None

    def _reschedule_closing(self):
        if self.closing_event is not None:
            self.scheduler.cancel(self.closing_event)

        closing_time = self.last_activity_time + timedelta(self.timeout)
        self.scheduler.enterabs(closing_time.timestamp(), 1, self.close())

    @staticmethod
    def _generate_token():
        # todo
        return ""
