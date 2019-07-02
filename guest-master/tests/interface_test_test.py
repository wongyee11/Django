#!/usr/bin/env.python
# coding=utf-8
import requests
import unittest

class GetEventListTest(unittest.TestCase):
    '''查询发布会接口测试'''

    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        '''发布会id为空'''
        r = requests.get(self.url, params={'eid':''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")

    def test_get_event_error(self):
        '''发布会id不存在'''
        r = requests.get(self.url, params={'eid':'901'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], "query result is empty")

    def test_get_event_success(self):
        '''发布会id为1，查询成功'''
        r = requests.get(self.url, params={'eid':'1'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")
        self.assertEqual(result['data']['name'], "小米5发布会")
        self.assertEqual(result['data']['address'], "北京国家会议中心")
        self.assertEqual(result['data']['start_time'], "2019-06-16T19:09:59")

if __name__ == '__main__':
    unittest.main()

'''
未集成unittest单元测试框架
#查询发布会接口
url = "127.0.0.1:8000/api/get_event_list/"
r = requests.get(url, params={'eid':'1'})   #查询发布会接口请求类型为GET，所以，通过get()方法调用。第一个参数为调用接口的URL地址，params指定接口的入参，将参数定义为字典。
result = r.json()

#断言接口返回值
assert result['status'] == 200
assert result['message'] == "success"
assert result['data']['name'] == "XX产品发布会"
assert result['data']['address'] == "北京国家会议中心"
assert result['data']['start_time'] == "2019-06-16T19:09:59"
'''