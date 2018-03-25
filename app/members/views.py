import requests
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from config import settings

User = get_user_model()


# Create your views here.

def facebook_login(request):
    # code로부터 AccessToken 가져오기
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    # 페이스북 로그인 버튼을 누른 후, 사용자가 승인하면 redirect_url에 GET parameter로 'code'가 전송됨
    # 이 값과 client_id, secret을 사용해서 Facebook서버에서 access_token을 받아와야 함
    code = request.GET.get('code')
    # 이전에 페이스북 로그인 버튼을 눌렀을 때, 'code'를 다시 전달받은 redirect_url값으로 그대로 사용
    redirect_uri = 'http://localhost:8000/members/login/'

    # 아래 엔드포인트에 get요청을 보냄
    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url, params)

    # 전송받은 json 결과값을 python 객체로 반환
    response_dict = response.json()

    for key, value in response_dict.items():
        print(f'{key}:{value}')

    # GraphAPI의 me 엔드포인트에 Get요청 보내기

    url = "https://graph.facebook.com/v2.12/me"
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
        ])
    }

    response = requests.get(url, params)
    response_dict = response.json()
    print(response_dict)

    # Get요청으로 받은 정보
    # 애플리케이션 별로 사용자에게 주어지는 id
    facebook_id = response_dict['id']
    name = response_dict['name']
    url_picture = response_dict['picture']['data']['url']

    # login 기능 추가필요함
    # Facebook_id가 username인 User가 존재할 경우
    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)

    # 존재하지 않는 경우
    else:
        user = User.objects.create_user(
            username=facebook_id,
        )

    return render(request, 'login.html')
