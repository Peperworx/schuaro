from schuaro.utilities import global_classes
import requests
import webbrowser
import urllib.parse
import secrets
import hashlib
class SchuaroClient:
    def __init__(self, schuaro_uri: str, client_id: str, client_secret: str):
        """
            Schuaro client.
        """
        
        # Set the schuaro_uri
        self.schuaro_uri = schuaro_uri

        # Set the client details
        self.client_id = client_id
        self.client_secret = client_secret
    
    def authorization_code_request(self, authcode: str, code_verifier: str, redirect_uri: str):
        """
            Requests a token from schuaro using an authorization code.
            The redirect uri sent in this MUST match the redirect uri for the original request.
        """

        post_data = global_classes.OAuthTokenRequest(
            grant_type="authorization_code"
        )

        # Set the authcode
        post_data.code = authcode

        # Redirect uri
        post_data.redirect_uri = redirect_uri

        # Set the code_verifier
        post_data.code_verifier = code_verifier

        # Send the request
        req = requests.post(
            f'http://{self.schuaro_uri}{"" if self.schuaro_uri.endswith("/") else "/"}users/token',
            dict(post_data)
        )

        print(req)


    def generate_login_url(self, redirect_uri: str, scope: list[str] = ["me"]):
        """
            Generates a login url, also returns the state and code_verifier
        """

        # Generate code_verifier
        code_verifier = hex(secrets.randbits(32))[2:]

        # Generate state
        state = hex(secrets.randbits(32))[2:]

        # URL params
        get_data = {
            "code_challenge": hashlib.sha256(code_verifier.encode()).hexdigest(),
            "code_challenge_method":"S256",
            "client_id":self.client_id,
            "state": state,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(scope)
        }

        # Encode
        encoded = urllib.parse.urlencode(get_data)

        # The uri
        uri = f'http://{self.schuaro_uri}{"" if self.schuaro_uri.endswith("/") else "/"}login?{encoded}'

        return uri,