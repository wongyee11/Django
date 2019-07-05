# coding=utf-8
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class GetEventListTest(unittest.TestCase):
    ''' 查询发布会信息（带用户认证）'''

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_get_event_list/"
        self.auth_user = ('admin', 'admin123456')

    def tearDown(self):
        print(self.result)

    def test_get_event_list_auth_null(self):
        ''' auth为空 '''
        r = requests.get(self.base_url, params={'eid':''})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertEqual(self.result['message'], 'user auth null')

    def test_get_event_list_auth_error(self):
        ''' auth错误 '''
        r = requests.get(self.base_url, auth=('abc','123'), params={'eid':''})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'], 'user auth fail')

    def test_get_event_list_eid_null(self):
        ''' eid 参数为空 '''
        r = requests.get(self.base_url, auth=self.auth_user, params={'eid':''})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_get_event_list_eid_error(self):
        ''' eid=901 查询结果为空 '''
        r = requests.get(self.base_url, auth=self.auth_user, params={'eid':901})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    def test_get_event_list_eid_success(self):
        ''' 根据 eid 查询结果成功 '''
        r = requests.get(self.base_url, auth=self.auth_user, params={'eid':1})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        #u'我是含有中文字符组成的字符串'代表是对字符串进行unicode编码,中文必须表明所需编码, 否则一旦编码转换就会出现乱码.
        self.assertEqual(self.result['data']['name'],u'红米Pro发布会')
        self.assertEqual(self.result['data']['address'],u'北京会展中心')

    def test_get_event_list_name_result_empty(self):
        ''' 关键字‘abc’查询 '''
        r = requests.get(self.base_url, auth=self.auth_user, params={'name':'abc'})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    def test_get_event_list_name_find(self):
        ''' 关键字‘发布会’模糊查询 '''
        r = requests.get(self.base_url, auth=self.auth_user, params={'name':'发布会'})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        #self.assertEqual(self.result['data'][0]['name'],u'红米Pro发布会')
        #self.assertEqual(self.result['data'][0]['address'],u'北京会展中心')   [0] 是指的数据的第一条查询结果
        self.assertEqual(self.result['data'][0]['name'],u'红米Pro发布会')
        self.assertEqual(self.result['data'][0]['address'],u'北京会展中心')

if __name__ == "__main__":
    test_data.init_data()  # 初始化接口测试数据
    unittest.main()