#!/usr/bin/env.python
# coding=utf-8

from Cryptodome.Cipher import AES
import base64
import requests
import unittest
import json

class AES_Bug_Test(unittest.TestCase):

    def setUp(self):
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        self.base_url = "http://127.0.0.1:8000/api/sec_get_guest_list/"
        self.app_key = 'W7v4D60fds2Cmk2U'

    def encryptBase64(self,src):
        return base64.urlsafe_b64encode(src)

    def encryptAES(self,src, key):
        """
        生成AES密文
        """
        iv = b"1172311105789011"
        cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src).encode('utf-8'))
        return self.encryptBase64(ciphertext)

    def test_aes_interface(self):
        '''test aes interface'''
        payload = {'eid': '1', 'phone': '18011001100'}
        # 加密
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()
        r = requests.post(self.base_url,data = {"data":encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")

if __name__ == '__main__':
    unittest.main()