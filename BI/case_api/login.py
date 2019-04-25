import requests

class Login():
    def login(url):
        login_data = {
            "account": "cw-api",
            "password": "123",
            "code": "nvrW6OD4",
            "force_login": True,
            "t": "",
        }
        headers = None
        r = requests.post(url + "/api/user", headers, login_data)
        print("登录账号", r.status_code)
        r = r.json()
        print(r)
        token = r["data"]["token"]
        headers = {"Auth": token}
        kid = r["data"]["id"]
        return  headers,kid

# 此判断语句建议一直作为程序的入口
if __name__ == '__main__':
    pass