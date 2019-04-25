import unittest
import requests
from setting import server, login_data
from utils import get_db


class Base(unittest.TestCase):
    def setUp(self):
        print('setup')
        self.headers = None
        self.token = self.login()
        self.headers = {
            "Auth": self.token
        }

    def login(self):
        r = self.post('/api/user', login_data)

        token = r['data']['token']
        assert r['data']['token'] is not None
        return token

    @property
    def db(self):
        return get_db()

    def tearDown(self):
        pass

    def get(self, url, data):
        r = requests.get(server + url, headers=self.headers, params=data, timeout=5)
        assert r.status_code == 200
        assert r.json()
        return r.json()

    def post(self, url, data):
        r = requests.post(server + url, headers=self.headers, json=data, timeout=5)
        assert r.status_code == 200
        assert r.json()
        return r.json()

    def put(self, url, data):
        r = requests.put(server + url, headers=self.headers, json=data, timeout=5)
        assert r.status_code == 200
        assert r.json()
        return r.json()

    def delete(self, url, data):
        r = requests.delete(server + url, headers=self.headers, json=data, timeout=5)
        assert r.status_code == 200
        assert r.json()
        return r.json()

if __name__ == "__main__":
    unittest.main()
