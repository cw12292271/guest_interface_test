import requests
url = "https://admin.t5.site.webot.ai"

login_data = {
    "account": "cw-api",
    "password": "123",
    "code": "nvrW6OD4",
    "t": ""
}

print(url +'/api/user')
headers = None
r = requests.post(url +'/api/user', headers, login_data)
r = r.json()
print(r)
token = r['data']['token']
print(token)
headers = {'Auth': token}

immediate_data = {'cid':'1'}
r = requests.get(url=url + '/api/statistic/first_page/immediate', headers=headers,params=immediate_data)
result = r.json()
print(result)
print(result['data']['机器人会话量'])
print(r.status_code)

r = requests.get(url=url +'/api/user/logout',headers=headers)
print(r.status_code)
