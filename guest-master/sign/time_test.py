#!/usr/bin/env.python
# coding=utf-8
#from sign.models import Event
from django.db.utils import IntegrityError
import time

#event_time = Event.objects.get(id=eid).start_time
event_time = "2019-06-30 19:59:59"
etime = str(event_time).split(".")[0]
timeArray = time.strptime(event_time, "%Y-%m-%d %H:%M:%S")
e_time = int(time.mktime(timeArray))

print({"event_time":event_time})
print({"etime":etime})
print({"timeArray":timeArray})
print({"e_time":e_time})

#now_time = str(time.time())
ntime = str(time.time()).split(".")[0]
n_time = int(ntime)

#print({"now_time":now_time})
print({"ntime":ntime})
print({"n_time":n_time})

if n_time > e_time:
    print({"比较n_time和e_time的大小n_time>e_time时":n_time})
else:
    print({"比较n_time和e_time的大小n_time<e_time时":e_time})