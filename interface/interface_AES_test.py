from Crypto.Cipher import AES
import base64
import requests
import unittest
import json


class AESTest(unittest.TestCase):

    def setUp(self):
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.base_url = "http://127.0.0.1:8001/api/sec_get_guest_list/"

    def tearDown(self):
        print(self.result)

    def encryptBase64(self,src):
        return base64.urlsafe_b64encode(src)

    def encryptAES(self,src):
        """生成AES 密文"""
        key = b'W7v4D60fds2Cmk2U'
        iv = b"1172311105789011"
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        return self.encryptBase64(ciphertext)

    def test_aes_interface(self):
        """test aes interface"""
        payload = {'eid': '1', 'phone': '13511001100'}
        # 加密
        encoded = self.encryptAES(json.dumps(payload)).decode()
        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], "success")

    def test_get_guest_list_eid_null(self):
        """ eid 参数为空"""
        payload = {'eid': '','phone': ''}
        encoded = self.encryptAES(json.dumps(payload)).decode()
        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'eid cannot be empty')

    def test_get_event_list_eid_error(self):
        """ 根据eid 查询结果为空"""
        payload = {'eid': '901','phone': ''}
        encoded = self.encryptAES(json.dumps(payload)).decode()
        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    def test_get_event_list_eid_success(self):
        """ 根据eid 查询结果成功"""
        payload = {'eid': '1','phone': ''}
        encoded = self.encryptAES(json.dumps(payload)).decode()
        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data'][0]['realname'],'alen')
        self.assertEqual(self.result['data'][0]['phone'],'13511001100')

    def test_get_event_list_eid_phone_null(self):
        """ 根据eid 和phone 查询结果为空"""
        payload = {'eid':2,'phone':'10000000000'}
        encoded = self.encryptAES(json.dumps(payload)).decode()
        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    def test_get_event_list_eid_phone_success(self):
        """ 根据eid 和phone 查询结果成功"""
        payload = {'eid':1,'phone':'13511001100'}
        encoded = self.encryptAES(json.dumps(payload)).decode()
        r = requests.post(self.base_url, data={"data": encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['realname'],'alen')
        self.assertEqual(self.result['data']['phone'],'13511001100')