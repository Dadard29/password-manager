from requests import Session, get


class Caller(object):
    endpoint_session = '/session'
    endpoint_directory = '/database/directory'
    endpoint_entry = '/database/entry'

    @staticmethod
    def check_up(host: str):
        try:
            r = get(host)
            return r.status_code == 404
        except:
            return False

    def __init__(self, host, key: int):
        self.host = host
        self.http = Session()

        r = self.http.post(
            self._get_url(self.endpoint_session),
            headers={'key': str(key)}
        )
        if r.status_code != 201:
            raise TypeError(r.json()['message'])

        self.session = r.json()['body']['session']
        token = r.json()['body']['token']
        self.http.headers = {
            'Authorization': token
        }

    def _get_url(self, endpoint):
        return self.host + endpoint

    # session
    def get_session(self):
        return self.http.get(self._get_url(self.endpoint_session))

    def delete_session(self):
        return self.http.delete(self._get_url(self.endpoint_session))

    # entries
    def post_entry(self, path: str, entry_name: str, value: str, metas: dict):
        p = dict(path=path, entry_name=entry_name)
        body = {
            'value': value,
            'metas': metas
        }
        return self.http.post(self._get_url(self.endpoint_entry), json=body, params=p)

    def get_entry(self, path, entry_name):
        p = dict(path=path, entry_name=entry_name)
        return self.http.get(self._get_url(self.endpoint_entry), params=p)

    def update_entry(self, path, entry_name, value: str, metas: dict):
        p = dict(path=path, entry_name=entry_name)
        body = {
            'value': value,
            'metas': metas
        }
        return self.http.put(self._get_url(self.endpoint_entry), json=body, params=p)

    def delete_entry(self, path, entry_name):
        p = dict(path=path, entry_name=entry_name)
        return self.http.delete(self._get_url(self.endpoint_entry), params=p)

    # directories
    def post_directory(self, path, dir_name):
        p = dict(path=path, dir_name=dir_name)
        return self.http.post(self._get_url(self.endpoint_directory), params=p)

    def get_directory(self, path, dir_name):
        p = dict(path=path, dir_name=dir_name)
        return self.http.get(self._get_url(self.endpoint_directory), params=p)

    def delete_directory(self, path, dir_name):
        p = dict(path=path, dir_name=dir_name)
        return self.http.delete(self._get_url(self.endpoint_directory), params=p)
