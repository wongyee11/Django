from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")   #在页面上显示字符串
    return render(request , "index.html")  # 在页面上显示HTML页面


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username' , '')
        password = request.POST.get('password' , '')
# 使用authenticate()函数认证给出的用户名和密码。它接受两个参数：username和password，并且会在用户名密码正确的情况下返回一个user对象，否则authenticate()返回None。
        user = auth.authenticate(username=username , password=password)
        '''
        if  username == 'admin' and password == 'admin123':
            response = HttpResponseRedirect('/event_manage/')
            response.set_cookie('user', username, 3600)     #添加浏览器cookie
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
        '''
        if user is not None:
            auth.login(request , user)  # 登录
            request.session['user'] = username  # 将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')  # 对路径进行重定向，将登录成功之后的请求指向/event_manage/目录
            return response
        else:
            return render(request , 'index.html' , {'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')      #读取浏览器cookie
    username = request.session.get('user' , '')  # 读取浏览器session
    return render(request , "event_manage.html" , {"user": username})  # 将读取自cookie的“user”值与event_manage.html页面一起返回
