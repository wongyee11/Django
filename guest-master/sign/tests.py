#!/usr/bin/env.python
# coding=utf-8
from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User

#Create your tests here.
class ModelTest(TestCase):
    '''模型测试'''

    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address='shenzhen', start_time='2019-06-19 9:19:59')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='13711001101', email='alen@mail.com', sign=False)

    def test_event_models(self):
        '''测试发布会表'''
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        '''测试嘉宾表'''
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)

#编写index视图的测试用例
class IndexPageTest(TestCase):
    '''测试index登录首页'''

    def test_index_page_render_index_template(self):
        ''' 断言是否用给定的index.html模版响应'''
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

#编写登录动作的测试用例
class LoginActionTest(TestCase):
    '''测试登录动作'''

    def setUp(self):
        '''初始化，调用User.objects.create_user创建登录用户数据'''
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        '''测试添加用户'''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        '''测试用户名密码为空'''
        test_data = {'username':'','password':''}
        #通过post()方法请求'/login_aciton/'路径测试登录功能
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        # assertIn()方法断言返回的HTML页面中是否包含指定的提示字符串
        self.assertIn(b"username or password null!", response.content)

    def test_login_action_username_password_error(self):
        '''测试用户名密码错误'''
        test_data = {'username':'abc','password':'123'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        '''测试登录成功'''
        test_data = {'username':'admin','password':'admin123456'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 302)

#编写发布会管理的测试用例
class EventManageTest(TestCase):
    '''发布会管理'''

    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(name="xiaomi5",limit=2000,address='beijing',
                             status=1,start_time='2019-6-19 9:59:59')
        self.login_user = {'username':'admin','password':'admin123456'}

    def test_event_mange_success(self):
        '''测试发布会：xiaomi5'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_mange_search_success(self):
        '''测试发布会搜索'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/',{"name":"xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

#编写嘉宾管理的测试用例
class GuestManageTest(TestCase):
    '''嘉宾管理'''

    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address="beijing",
                             status=1,start_time='2019-6-19 9:59:59')
        Guest.objects.create(realname="alen",phone=18611001100,
                             email='alen@mail.com',sign=0,event_id=1)
        self.login_user = {'username':'admin','password':'admin123456'}

    def test_guest_mange_success(self):
        '''测试嘉宾信息：alen'''

        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

    def test_guest_mange_search_success(self):
        '''测试嘉宾搜索'''

        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_phone/', {"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

#编写用户签到的测试用例
class SignIndexActionTest(TestCase):
    '''发布会签到'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="xiaomi5", limit=2000,
                             address="beijing", status=1, start_time='2019-6-19 9:59:59')
        Event.objects.create(id=2, name="oneplus4", limit=2000,
                             address="shenzhen", status=1, start_time='2019-6-19 19:59:59')
        Guest.objects.create(realname="alen", phone=18611001100,
                             email="alen@mail.com", sign=0, event_id=1)
        Guest.objects.create(realname="una", phone=18611001101,
                             email="una@mail.com", sign=1, event_id=2)
        self.login_user = {'username':'admin','password':'admin123456'}

    def test_sign_index_action_phone_null(self):
        '''手机号为空'''

        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone":""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        '''手机号或发布会id错误'''

        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        '''用户已签到'''

        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {"phone":18611001101})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        '''签到成功'''

        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)



'''
运行所有用例：
python3 manage.py test

运行sign应用下的所有用例：
python3 manage.py test sign

运行sign应用下的tests.py文件用例：
python3 manage.py test sign.tests

运行sign应用下的tests.py文件中的 GuestManageTest 测试类：
python3 manage.py test sign.tests.GuestManageTest

运行sign引用tests.py测试文件下的ModelTest测试类。
python manage.py test sign.tests.ModelTest

运行sign应用下的tests.py文件中ModelTest测试类下面的test_event_models测试方法（用例）。
python manage.py test sign.tests.ModelTest.test_event_models

使用-p（或--pattern）参数模糊匹配测试文件。
python manage.py test -p test*.py

......


'''