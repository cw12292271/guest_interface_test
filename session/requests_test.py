import time
from pprint import pprint

import requests

data = {"msg": "测试"}

chat_data = requests.get("http://127.0.0.1:8802/chat", params=data).json()

time.sleep(5)

print(chat_data)

history = requests.get("http://127.0.0.1:8802/history").json()
#
time.sleep(5)
#
pprint(history)
