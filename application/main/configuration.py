import os

class BaseConfiguration:
    """
        `BaseConfiguration` is used to store the environment variables defined in the .env file or exported directly into the system itself.
        For now it only contains 2 variables:
        
        `SCOPES` - which define the type of access you will have on the API, you can read about it more [here](https://developers.google.com/workspace/guides/configure-oauth-consent)
        
        `CREDENTIALS_FILE_NAME` - To have access to GCP you will need to have a `.json` file which you can generate on the GCP platform when you are creating the user, but the TLDR is this
        the authentication on this project is done using service_account which is perfectly fine if you want to access only your files but if you want access to file which the owner is not you 
        you will be restricted from donig that, in this case you will setup OAuth2
    """

    SCOPES = os.environ.get("SCOPES").strip().split(",")
    # CREDENTIALS_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    CREDENTALS = {
        "type": os.environ.get("TYPE"),
        "project_id": os.environ.get("PROJECT_ID"),
        "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
        "private_key": os.environ.get("PRIVATE_KEY"),
        "client_email": os.environ.get("CLIENT_EMAIL"),
        "client_id": os.environ.get("CLIENT_ID"),
        "auth_uri": os.environ.get("AUTH_URI"),
        "token_uri": os.environ.get("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("CLIENT_PROVIDER_X509_CERT_URL"),
    }