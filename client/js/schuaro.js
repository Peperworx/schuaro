class Schuaro {
    constructor(schuaro_uri, login_uri) {
        /*
            - schuaro_uri
                The URI where the scuaro server is mounted
            - login_uri
                The URI of your local token request server.
                Authorization code requests must be done on the server, as 
                    they require to send a client secret
        */

        // Set the schuaro_uri
        this.schuaro_uri = schuaro_uri;

        // Set the login_uri
        this.login_uri = login_uri;

    }
}