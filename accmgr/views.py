import json
from hashlib import md5
from datetime import datetime

import requests
from ipware.ip import get_real_ip, get_ip

from django.shortcuts import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import UserProfile


def fbauth(request):
    """Log in with Facebook account."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['id']
        access_token = data['token']
        user_set = User.objects.filter(username=username)
        if user_set:
            user = user_set[0]
        else:
            url = 'https://graph.facebook.com/{uid}?fields=id,name,email&access_token={access_token}'.format(
                uid=username,
                access_token=access_token,
            )
            resp = requests.get(url)
            print('---------------------------')
            print(resp.url)
            print('---------------------------')
            d = resp.json()
            email = d.get('email')
            password = md5(str(datetime.now()).encode('utf-8')).hexdigest()
            user = User.objects.create_user(username=username, password=password)
            displayname = data['name']
            ip = get_real_ip(request)
            ip = ip if ip else get_ip(request)
            profile = UserProfile.objects.create(
                user=user,
                username=username,
                displayname=displayname,
                email=email,
                ip=ip,
            )
            profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponse('ok')
    else:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    raise Http404
