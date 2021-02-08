from schuaro.utilities import global_classes
import requests

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
            f"{self.schuaro_uri}/users/token",
            post_data
        )


        