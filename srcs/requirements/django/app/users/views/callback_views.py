import os
import requests
from django.shortcuts import redirect, reverse
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from users.auth.oauth42 import Token
from users.models import Profile

def oauth_callback(request):
    authorization_code = request.GET.get('code')
    returned_state = request.GET.get('state')

    if returned_state != settings.CLIENT.state:
        return HttpResponse("Invalid state parameter", status=400)

    if not authorization_code:
        return HttpResponse("Authorization code not found", status=400)

    try:
        token = settings.CLIENT.get_token(authorization_code)
    except Exception as e:
        return HttpResponse(f"Error during token exchange: {str(e)}", status=400)
    
    request.session['token'] = token
    return redirect(reverse("dashboard"))

CustomUser = get_user_model()

def dashboard(request):
    access_token = request.session.get('token')
    if not access_token:
        return redirect(reverse("home"))

    try:
        data = Token(access_token).get("/v2/me")
    except Exception as e:
        return HttpResponse(f"Error fetching user data: {str(e)}", status=400)

    login, email, image_url = data.get("login"), data.get("email"), data.get("image", {}).get("link", "")
    user = get_or_create_user(login, email)
    update_or_create_profile(user, image_url)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user)

    return redirect(reverse("profile"))

def get_or_create_user(username, email):
    user, created = CustomUser.objects.get_or_create(username=username, defaults={'email': email})
    if not created:
        user.email = email
        user.save()
    return user

def update_or_create_profile(user, image_url):
    profile, created = Profile.objects.get_or_create(user=user)
    img_name = f"{user.username}_profile.jpg"
    img_path = os.path.join(settings.MEDIA_ROOT, img_name)

    if os.path.exists(img_path):
        profile.image.name = img_name
        profile.save()
        return

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(img_path, 'wb') as f:
            f.write(response.content)
        profile.image.name = img_name
        profile.save()
        profile.refresh_from_db()
    except requests.exceptions.RequestException as e:
        pass
    except Exception as e:
        pass