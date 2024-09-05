import requests
import uuid
import urllib.parse
import json


class Oauth42:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id: str = client_id
        self.redirect_uri: str = redirect_uri
        self.scope: str = "public"
        self.state: str = str(uuid.uuid4())
        self.response_type: str = "code"
        self.client_secret: str = client_secret
        self.token_url: str = "https://api.intra.42.fr/oauth/token"


    @property
    def auth_url(self) -> str:
        """ where to send user for authentication """
        if not self.client_id or not self.redirect_uri or not self.state:
            raise Exception("MissingData: couldn't generate authorization url")

        base_auth_url = "https://api.intra.42.fr/oauth/authorize?"
        params = f"client_id={self.client_id}\
            &redirect_uri={urllib.parse.quote_plus(self.redirect_uri)}\
            &scope={self.scope}\
            &response_type={self.response_type}\
            &state={self.state}"
        
        return f"{base_auth_url}{params}" 


    def get_token(self, code) -> str:
        """ exchange temporary code for access token """
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code != 200:
            return
        data = response.json()
        return data["access_token"]


class Token():
    def __init__(self, token: json) -> None:
        self.access_token: str = token
        self.base_url = "https://api.intra.42.fr"


    def get(self, endpoint: str) -> json:
        """ Fetch data based on endpoint """
        if not self.access_token:
            return
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        url = self.base_url + endpoint
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"BadResponse: code {response.status_code}: {response}")
        return response.json()