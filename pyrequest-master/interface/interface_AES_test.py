# coding=utf-8
from Cryptodome.Cipher import AES
import base64
import requests
import unittest
import json


class AESTest(unittest.TestCase):

    def setUp(self):
        #因为接口参数的个数和长度是不固定的，所以加密字符串的长度不可控。为了解决这个问题，还需要对字符串长度进行处理，使它的长度符合encrypt()方法的要求
        BS = 16
        #这是函数式编程的用法，通过lambda定义匿名函数来对字符串进行补足，使其长度变为16、24或32位。
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        self.base_url = "http://127.0.0.1:8000/api/sec_get_guest_list/"
        # 首先，定义好 app_key 和接口参数，app_key是密钥只能告诉给合法的接口调用者，一定要保密噢！使用字典格式来存放接口参数。
        self.app_key = 'W7v4D60fds2Cmk2U'

    def encryptBase64(self,src):
        #通过encrypt()方法生成的字符串太长，于是通过base64模块的urlsafe_b64encode()方法对AES加密字符串进行二次加密。
        return base64.urlsafe_b64encode(src)

    def encryptAES(self,src, key):
        """
        生成AES密文
        """
        # IV同样是保密的，我们知道它必须是16位。
        iv = b"1172311105789011"
        cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        #通过encrypt()方法对src（JSON格式的接口参数）生成加密字符串。但是，encrypt()方法要求被加密的字符串长度必须为16、24或32位。
        ciphertext = cryptor.encrypt(self.pad(src).encode('utf-8'))
        return self.encryptBase64(ciphertext)

    def test_aes_interface(self):
        '''test aes interface'''
        payload = {'eid': '1', 'phone': '18011001100'}
        # 加密
        #通过json.dumps()方法将payload字典转化为JSON格式，和app_key一起作为encryptAES()方法的参数，用于生成AES加密字符串。
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        #接口参数的加密过程结束。将加密后的字符串作为data参数发送接口请求。
        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")

    def test_get_guest_list_eid_null(self):
        ''' eid 参数为空 '''
        payload = {'eid': '','phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'eid cannot be empty')

    def test_get_event_list_eid_error(self):
        ''' 根据 eid 查询结果为空 '''
        payload = {'eid': '901','phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_list_eid_success(self):
        ''' 根据 eid 查询结果成功 '''
        payload = {'eid': '1','phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data'][0]['realname'],'alen')
        self.assertEqual(result['data'][0]['phone'],'18011001100')

    def test_get_event_list_eid_phone_null(self):
        ''' 根据 eid 和phone 查询结果为空 '''
        payload = {'eid':2,'phone':'10000000000'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_list_eid_phone_success(self):
        ''' 根据 eid 和phone 查询结果成功 '''
        payload = {'eid':1,'phone':'18011001100'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['realname'],'alen')
        self.assertEqual(result['data']['phone'],'18011001100')

if __name__ == '__main__':
    unittest.main()
