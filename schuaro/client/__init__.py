from schuaro.utilities import global_classes
import requests
import webbrowser
import urllib.parse
import secrets
import hashlib
import http.server
import socketserver
import os
import time
import threading
import base64
class AuthComplete(Exception):
    pass

class TCPServer(socketserver.TCPServer):
    auth_complete:bool=False
class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=UTF-8')
        self.end_headers()
        with open(os.path.join(os.path.dirname(__file__),"response.html"), 'rb') as f:
            while c := f.read(1024):
                self.wfile.write(c)
        if not self.server.has_served:
            params = {i.split("=")[0]:i.split("=")[1] for i in self.path.split("?")[1].split("&")}
            self.server.has_served = params
        return
            
        
        



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

        # Set the client id
        post_data.client_id = self.client_id
        post_data.client_secret = self.client_secret

        # Send the request
        req = requests.post(
            f'{self.schuaro_uri}{"" if self.schuaro_uri.endswith("/") else "/"}users/token',
            dict(post_data)
        )

        print(req.content)
        print()

    def generate_login_url(self, redirect_uri: str, scope: list[str] = ["me"]):
        """
            Generates a login url, also returns the state and code_verifier
        """

        # Generate code_verifier
        code_verifier = hex(secrets.randbits(32))

        # Generate state
        state = hex(secrets.randbits(32))[2:]
        print(hashlib.sha256(code_verifier.encode()).hexdigest())
        # URL params
        get_data = {
            "code_challenge": base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode(),
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
        uri = f'{self.schuaro_uri}{"" if self.schuaro_uri.endswith("/") else "/"}login?{encoded}'

        return uri,state,code_verifier
    
    def initiate_callback(self, callback, scope: list[str] = ["me"]):
        """
            Authenticates and calls callback when done.
        """
        # Get the server class ready
        httpd = TCPServer(("", 0), HttpRequestHandler)
        httpd.has_served = None
        
        # Start the server
        t = threading.Thread(target=httpd.serve_forever)
        t.start()
        
        # Redirect uri
        redirect_uri = f"http://localhost:{httpd.server_address[1]}"

        # Generate the url
        url = self.generate_login_url(
                redirect_uri,
                scope=scope
            )

        # Open the browser
        webbrowser.open(
            url[0]
        )

        # Say that we are awaiting response
        print(f"Awaiting Response at http://localhost:{httpd.server_address[1]}")

        # Wait until we have recieved the request
        while not httpd.has_served:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                httpd.shutdown()
                raise
        # Shutdown
        httpd.shutdown()

        # Say that authentication detected
        print("Authentication detected")

        # Grab the query parameters
        params = httpd.has_served

        # Verify state
        if params.get("state") != url[1]:
            raise ValueError("States are not equal. This may mean a man in the middle attack")
        
        # Now request the token via authcode
        token = self.authorization_code_request(
            params.get("code"),
            url[2],
            redirect_uri
        )
        print(token)