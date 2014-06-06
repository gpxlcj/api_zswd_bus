#! -*- coding:utf-8 -*-
from random import randint,choice
import re

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import send_mail

from bus.models import *
from bus.json import render_json, return_positiondata

#激活邮件发送
def send_activate_mail(emailurl, activatecode):
    try:
        activateurl = u'bus.ziqiang.net/activate/'+activatecode
        title = u'BusLover恭喜您注册成功'
        message = u'请点击或手动访问下面地址来激活您的帐号'+activateurl
        send_mail(title,activateurl,'gpxlcj@126.com',[emailurl])
        return True
    except:
        return False

#用户注册
def user_register(request):
    if request.method == 'POST':

#        if request.POST.get('user_id'):
#            newuser_id = request.POST.get('user_id')
#            for i in WantInfoUser.objects.all():
#                if i.user_id == newuser_id:
#                    return render_json({'status':'error_sameid'})
#        else:
#            return render_json({'status':'error_id'})
        if re.match(r"(.)+@(.)+\.(.)+", str(request.POST.get('user_email'))):
            newuser_email = str(request.POST.get('user_email'))
            for i in Email.objects.all():
                if i.email_name == newuser_email:
                    return render_json({'status':'error_sameemail'})
            new_email = Email(email_name = newuser_email)
            new_email.save()
        else:
            return render_json({'status':'error_email'})

        if request.POST.get('user_password'):
            newuser_password = request.POST.get('user_password')
        else:
            return render_json({'status':'error_password'})
        if request.POST.get('user_password_confirm'):
            if request.POST.get('user_password_confirm')==newuser_password:
                pass
            else:
                return render_json({'status':'error_samepassword'})
        else:
            return render_json({'status':'error_repeatpassword'})
#发送激活邮件

#        activatecode = ''
#        for i in range(8, 20):
#            activatecode += str(chr(choice([randint(48, 58), randint(65, 91), randint(97, 103)])))
#        send_activate_mail(newuser_email, activatecode)
        infouser = WantInfoUser(user_password = newuser_password, user_email = new_email)
        infouser.save()
        return render_json({'status':'success'})
    return HttpResponse("wrong information")

#用户登录
def user_login(request):
    if request.method == 'POST':
        if request.POST.get('user_email'):
            for i in WantInfoUser.objects.all():
                if str(i.user_email) == str(request.POST.get('user_email')):
                    now_user = i
                    break
            else:
                return render_json({'status':'error_exist'})
        else:
            return render_json({'status':'error_blankid'})
        if request.POST.get('user_password'):
            if now_user.user_password == request.POST.get('user_password'):
                pass
            else:
                return render_json({'status':'error_password'})
        else:
            return render_json({'status':'error_blankpassword'})
        return render_json({'status':now_user.user_login()})
    return render_json({'status':'error'})

#用户登出
def user_logout(request):
    if request.method == 'POST':
        if request.POST.get('user_email'):
            for i in WantInfoUser.objects.all():
                if str(i.user_email) == str(request.POST.get('user_email')):
                    now_user = i
                    break
            return render_json({'status':now_user.user_logout()})
        else:
            return render_json({'status':'error'})
    else:
        return render_json({'status':'error'})
