# coding: utf-8

# !pip install git+https://github.com/centrifugal/centrifuge-python.git

# !pip install cent

import asyncio
import time

import requests
from centrifuge import Client, Credentials
from flask import Flask, request
from flask import jsonify
import json

app = Flask(__name__)

message = []


def weboskcet():
    params = {
        'uid': '123f037765aa4ac6a77c978da1e2e84b',
        'code': '982ea76e92a211e787e1000c2913faa4',
        'ref': 'qd1'
    }
    r = requests.get('http://admin.t7.site.webot.ai/api/chats/websocket', params=params)
    return r.json()['data']


def chat(text):
    params = {
        'uid': '123f037765aa4ac6a77c978da1e2e84b',
        'code': '982ea76e92a211e787e1000c2913faa4',
        'ref': 'qd1'
    }
    data = {"uid": "123f037765aa4ac6a77c978da1e2e85b", "source": "h5", "msg_type": "text", "media": {}, "text": text}
    r = requests.post('http://admin.t7.site.webot.ai/api/chat', params=params, data=json.dumps(data))
    time.sleep(5)
    print(r.text)
    return r.json()


weboskcet()
# chat('哈哈哈')


async def run():
    # Generate credentials.
    # In production this must only be done on backend side and you should
    # never show secret to client!
    data = weboskcet()
    print(data)
    credentials = Credentials(data['user'], data['timestamp'], '', data['token'])
    address = data['url']

    async def connect_handler(**kwargs):
        print("Connected", kwargs)

    async def disconnect_handler(**kwargs):
        print("Disconnected:", kwargs)

    async def connect_error_handler(**kwargs):
        print("Error:", kwargs)

    client = Client(
        address, credentials,
        on_connect=connect_handler,
        on_disconnect=disconnect_handler,
        on_error=connect_error_handler
    )

    await client.connect()

    async def message_handler(**kwargs):
        print("Message:", kwargs)
        message.append(kwargs)

    async def join_handler(**kwargs):
        print("Join:", kwargs)

    async def leave_handler(**kwargs):
        print("Leave:", kwargs)

    async def error_handler(**kwargs):
        print("Sub error:", kwargs)

    await client.subscribe(
        data['user'],
        on_message=message_handler,
        on_join=join_handler,
        on_leave=leave_handler,
        on_error=error_handler
    )


@app.route("/chat")
def chat_test():
    content = request.args.get("msg")
    chat(content)
    # chat("哈")
    # time.sleep(5)

    return jsonify({"code": 0, "msg": "success"})


@app.route("/history")
def history():
    return jsonify({"code": 0, "msg": "success", "data": message})


def run_flask():
    app.run(debug=False, host='0.0.0.0', port=8802)


def run_flask_on_thread():
    import threading
    t = threading.Thread(target=run_flask)
    t.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    run_flask_on_thread()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        loop.close()
