from requests import Session


class Caller(object):

    endpoint_session = '/session'
    endpoint_database = '/database'

    def __init__(self, host, key):
        self.host = host
        self.http = Session()
        r = self.http.post(
            self.get_url(self.endpoint_session),
            headers={'key': key}
        )
        if r.status_code != 201:
            raise TypeError(r.json()['message'])

        self.session = r.json()['body']['session']
        token = r.json()['body']['token']
        self.http.headers = {
            'Authorization': token
        }

    def get_url(self, endpoint):
        return self.host + endpoint

    def get_session(self):
        return self.http.get(self.get_url(self.endpoint_session))

    def delete_session(self):
        return self.http.delete(self.get_url(self.endpoint_session))

    def get_secret(self, group, entry):
        return self.http.get(self.get_url(self.endpoint_database + f'/{group}/{entry}'))

    def get_group(self, group):
        return self.http.get(self.get_url(self.endpoint_database + f'/{group}'))
