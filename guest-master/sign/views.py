#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Event,Guest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

logger = logging.getLogger(__name__)


# Create your views here.
# 首页(登录)
def index(request):
    return render(request,"index.html")


# 登录动作
def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username == '' or password == '':
            return render(request,"index.html",{"error":"username or password null!"})

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user) # 验证登录
            response = HttpResponseRedirect('/event_manage/') # 登录成功跳转发布会管理
            request.session['username'] = username    # 将 session 信息写到服务器
            return response
        else:
            return render(request,"index.html",{"error":"username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request,"index.html")

# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response


# 发布会管理（登录之后默认页面）
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('username', '')
    return render(request, "event_manage1.html", {"user": username,"events":event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage1.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')
    #return render(request , "guest_manage.html" , {"user": username , "guests": guest_list})

    paginator = Paginator(guest_list, 2)   #页面显示条目数量
    #paginator = Paginator(guest_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage1.html", {"user": username, "guests": contacts})



# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    #return render(request , "guest_manage.html" , {"user": username ,
    #                                                "guests": guest_list ,
    #                                                "phone": search_phone})

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage1.html", {"user": username,
                                                   "guests": contacts,
                                                   "phone":search_phone})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)           # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)   # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index1.html', {'event': event,
                                               'guest':guest_data,
                                               'sign':sign_data})


# 前端签到页面
def sign_index2(request,event_id):
    event_name = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index2.html',{'eventId': event_id,
                                               'eventNanme': event_name})


# 签到动作
@login_required
def sign_index_action(request,event_id):

    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = 0   #计算发布会“已签到”的数量
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1

    phone =  request.POST.get('phone','')

    #查询手机号在Guest表中是否存在，如果不存在则提示用户“phone error”。
    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index1.html', {'event': event,'hint': 'phone error.',
                                                    'guest':guest_data,'sign':sign_data})

    #通过手机和发布会id两个条件来查询Guest表，如果结果为空，则说明手机号与发布会不匹配，将提示用户“event id or phone error.”。
    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index1.html', {'event': event,'hint': 'event id or phone error.',
                                                    'guest':guest_data,'sign':sign_data})

    #判断嘉宾的签到状态是否为True(1)，如果为True，则表示嘉宾已经签过到了，将提示用户“user has sign in.”。
    # 否则，说明嘉宾未签到，修改签到状态为1（已签到），提示用户“sign in success!”，并且显示嘉宾的姓名和手机号。
    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index1.html', {'event': event,'hint': "user has sign in.",
                                                    'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index1.html', {'event': event,'hint':'sign in success!',
            'user': result, #sign_index.html用的是guestuser
            'guest':guest_data,
            'sign':str(int(sign_data)+1)
            })


'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''
