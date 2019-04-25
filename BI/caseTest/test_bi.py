from datetime import timedelta

import requests

from BI.data.basic import *

headers = {"Cookie": 'Auth=15b7d8b2-fea0-11e8-9e4e-0242ac120005'}


def login():
    headers = None
    r = requests.post(base_url + "/api/user", headers, login_data)
    print("登录账号", r.status_code)
    r = r.json()
    print(r)
    token = r["data"]["token"]
    headers = {"Auth": token}
    print(headers)
    return headers


def api_robot_pandect():
    data = {'cid': cid, 'start': start, 'end': end}
    rep = requests.get(url=apis['机器人总览'], headers=headers, params=data)
    rep = rep.json()['data']
    # pprint(rep)
    return rep


def api_kf_overview():
    data = {'cid': cid, 'start': start, 'end': end, 'user_id': user_id}
    rep = requests.get(url=apis['客服总览'], headers=headers, params=data)
    rep = rep.json()['data']

    return rep


def api_kf_work_load():
    data = {'cid': cid, 'start': start, 'end': end}
    rep = requests.get(url=apis['客服工作量'], headers=headers, params=data)
    rep = rep.json()['data']['list']
    for rp in rep:
        if rp['id'] == user_id:
            rep = rp
    return rep


def api_kf_quality_work():
    data = {'cid': cid, 'start': start, 'end': end}
    rep = requests.get(url=apis['客服工作质量'], headers=headers, params=data)
    rep = rep.json()['data']['list']
    for rp in rep:
        if rp['id'] == user_id:
            rep = rp
    return rep


def api_kf_attendance():
    data = {'cid': cid, 'start': start, 'end': end, 'user_id': user_id}
    rep = requests.get(url=apis['客服考勤'], headers=headers, params=data)
    rep = rep.json()['data']
    for rl in rep['list']:
        if rl['姓名'] == user_id:
            return rl


def api_kf_work_load_details():
    data = {'cid': cid, 'start': start, 'end': end, 'user_id': user_id}
    rep = requests.get(url=apis['客服工作量'], headers=headers, params=data)
    # print(rep.url)
    rep = rep.json()['data']
    return rep


def api_visitor_overview():
    data = {'cid': cid, 'start': start, 'end': end}
    rep = requests.get(url=apis['访客'], headers=headers, params=data)
    rep = rep.json()['data']
    return rep


# pprint(api_kf_work_load_details())
# kf_attendance()
# api_visitor_overview()