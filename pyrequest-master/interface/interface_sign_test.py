# coding=utf-8
import unittest
import requests
from time import time
import hashlib
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class AddEventTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_add_event/"
        # api_key
        self.api_key = "&Guest-Bugmaster"
        # 当前时间，服务器的时间
        now_time = time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def tearDown(self):
        print(self.result)

    def test_add_event_request_error(self):
        '''请求方法错误'''
        r = requests.get(self.base_url)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10011)
        self.assertEqual(self.result['message'] , 'request error')

    def test_add_event_sign_null(self):
        ''' 签名参数为空 '''
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':'','sign':''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10012)
        self.assertEqual(self.result['message'] , 'user sign null')

    def test_add_event_time_out(self):
        ''' 请求超时 '''
        now_time = str(int(self.client_time) - 61)  #服务器时间减去请求的时间大于60，请求超时
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':now_time,'sign':'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10013)
        self.assertEqual(self.result['message'] , 'user sign timeout')

    def test_add_event_sign_error(self):
        ''' 签名错误 '''
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':self.client_time,'sign':'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10014)
        self.assertEqual(self.result['message'] , 'user sign error')

    def test_add_event_eid_exist(self):
        ''' id已经存在 '''
        payload = {'eid':1,'name':'小米5发布会','limit':2000,'address':"深圳宝体",'start_time':'2019','time':self.client_time,'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10022)
        self.assertEqual(self.result['message'] , 'event id already exists')

    def test_add_event_name_exist(self):
        ''' 名称已经存在 '''
        payload = {'eid':19,'name':'小米5发布会','limit':2000,'address':"深圳宝体",'start_time':'2019','time':self.client_time,'sign':self.sign_md5}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10023)
        self.assertEqual(self.result['message'] , 'event name already exists')

    def test_add_event_data_type_error(self):
        ''' 日期格式错误 '''
        payload = {'eid':19,'name':'一加5手机发布会','limit':2000,'address':"深圳宝体",'start_time':'2019','time':self.client_time,'sign':self.sign_md5}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 10024)
        self.assertIn('start_time format error.' , self.result['message'])

    def test_add_event_success(self):
        ''' 添加成功 '''
        payload = {'eid':19,'name':'一加5手机发布会','limit':2000,'address':"深圳宝体",'start_time':'2019-07-09 19:59:59','time':self.client_time,'sign':self.sign_md5}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'] , 200)
        self.assertEqual(self.result['message'] , 'add event success')


if __name__ == '__main__':
    test_data.init_data() # 初始化接口测试数据
    unittest.main()