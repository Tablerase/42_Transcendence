from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from ..auth.oauth42 import Token
from django.http import HttpResponse
from urllib.parse import urlencode


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


def dashboard(request):
    """
    Retrieve user data from the OAuth provider and display it.
    """
    # Retrieve the access token from the session
    access_token = request.session.get('token')
    
    if not access_token:
        print("No access token found in session.")  # Debug: No token found
        return redirect(reverse("home"))

    print(f"Access token found: {access_token}")  # Debug: Print access token

    # Use the Token class to make authorized requests
    token = Token(access_token)
    
    # Retrieve user data
    try:
        data = token.get("/v2/me")
        print(f"User data retrieved: {data}")  # Debug: Print the data fetched from the API
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")  # Debug: Print error if fetching fails
        return HttpResponse(f"Error fetching user data: {str(e)}", status=400)

    # Prepare the context for the dashboard
    context = {
        "name": f'{data.get("first_name", "")} {data.get("last_name", "")}',
        "email": data.get("email", ""),
        "image": data.get("image", {}).get("link", ""),  # Assuming 'image' key is a dictionary
        "data": data  # Pass entire data object for flexibility
    }

    return render(request, "users/profile/dashboard.html", context)