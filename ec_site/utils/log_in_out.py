from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import UserProfile
import json
from hashlib import sha1


def process_reg(user_name, user_id, password):
    s = sha1()
    s.update(password.encode("utf-8"))
    password_sha = s.hexdigest()
    UserProfile.objects.create(user_name=user_name, user_id=user_id, password=password_sha)


def process_login(request):
    user_id = request.POST.get('user_id', None)
    password = request.POST.get('password', None)
    user_obj = UserProfile.objects.filter(user_id=user_id).values()
    # 使用者存在
    if len(user_obj) == 1:
        # 密碼正確, 自動導入首頁
        s = sha1()
        s.update(password.encode("utf-8"))
        password_sha = s.hexdigest()
        if password_sha == user_obj[0]['password']:
            # 紀錄登入狀態至session
            request.session['user_id'] = user_id
            resp = redirect(reverse('home_page'))
            print(user_obj[0]['password'])
            print('########## 密碼正確, 自動導入首頁 ##########')
        # 密碼錯誤, 自動導回登入頁面
        else:
            resp = render(request, 'login/login.html')
            print(user_obj[0]['password'])
            print(password_sha)
            # 回彈錯誤視窗告訴用戶(待)

            print('########## 密碼錯誤, 自動導回登入頁面 ##########')
    # 使用者不存在, 自動導回登入頁面
    else:
        resp = render(request, 'login/login.html')
        print('########## 使用者不存在, 自動導回登入頁面 ##########')

    return resp


def process_logout(request):
    del request.session['user_id']
    resp = redirect(reverse('home_page'))
    return resp

def validate_login_state(request):
    user_id = request.session.get('user_id', None)
    is_logged_in = user_id is not None
    return is_logged_in