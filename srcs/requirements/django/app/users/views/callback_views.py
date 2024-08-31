import os
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from users.auth.oauth42 import Token
from users.models import Profile
import requests
from django.core.files.storage import default_storage

def oauth_callback(request):
    """
    Handle the callback from the OAuth provider.
    Exchange authorization code with access token and store it in the session.
    """
    # Retrieve the authorization code and state from the request
    authorization_code = request.GET.get('code')
    returned_state = request.GET.get('state')

    print(f"Authorization code: {authorization_code}")  # Debug: Print authorization code
    print(f"State returned: {returned_state}")  # Debug: Print state returned

    # Verify the state parameter to prevent CSRF attacks
    if returned_state != settings.CLIENT.state:
        return HttpResponse(f"Invalid state parameter", status=400)

    if not authorization_code:
        return HttpResponse("Authorization code not found", status=400)

    # Exchange the authorization code for an access token
    try:
        token = settings.CLIENT.get_token(authorization_code)
        print(f"Token received: {token}")  # Debug: Print the token received
    except Exception as e:
        print(f"Error during token exchange: {str(e)}")  # Debug: Print error if token exchange fails
        return HttpResponse(f"Error during token exchange: {str(e)}", status=400)
    
    # Store the token in the session
    request.session['token'] = token

    # Redirect to the dashboard view
    return redirect(reverse("dashboard"))

CustomUser = get_user_model()

def dashboard(request):
    """
    Retrieve user data from the OAuth provider, create or update the user,
    and log them in.
    """
    access_token = request.session.get('token')
    if not access_token:
        print("No access token found in session.")
        return redirect(reverse("home"))

    print(f"Access token found: {access_token}")

    # Retrieve user data from the OAuth provider
    try:
        data = Token(access_token).get("/v2/me")
        print(f"User data retrieved: {data}")
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return HttpResponse(f"Error fetching user data: {str(e)}", status=400)

    # Extract relevant user data
    login, email, image_url = data.get("login"), data.get("email"), data.get("image", {}).get("link", "")

    # Create or update the user in the database
    user = get_or_create_user(login, email)

    # Create or update the user's profile
    update_or_create_profile(user, image_url)

    # Set the backend for authentication and log the user in
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user)

    return redirect(reverse("profile"))


def get_or_create_user(username, email):
    """
    Creates or updates a user with the given username and email.
    """
    user, created = CustomUser.objects.get_or_create(username=username, defaults={'email': email})
    if not created:
        user.email = email
        user.save()
    return user

def update_or_create_profile(user, image_url):
    """
    Creates or updates the profile associated with the user, saves the image directly to the /media/ directory,
    and sets the image as the profile picture if it exists.
    """
    profile, created = Profile.objects.get_or_create(user=user)

    # Define the path and filename for the profile picture in the /media/ root directory
    img_name = f"{user.username}_profile.jpg"
    img_path = os.path.join(settings.MEDIA_ROOT, img_name)

    # Check if the image file already exists in /media/ and set it as the profile picture if it does
    if os.path.exists(img_path):
        print(f"Profile image found: {img_path}. Setting as profile image.")
        profile.image.name = img_name
        profile.save()
        return

    # Download the image from the provided URL and save it directly in the /media/ root directory
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Save the image directly into the /media/ directory
        with open(img_path, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded and saved profile image to: {img_path}")

        # Set the saved image as the profile picture
        profile.image.name = img_name
        profile.save()
        profile.refresh_from_db()  # Refresh to reflect updated data
        print(f"Profile updated successfully with image: {profile.image.url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading profile image: {e}")  # Handle download errors
    except Exception as e:
        print(f"Error saving profile: {e}")  # Handle other errors during the save operation