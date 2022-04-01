from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import webbrowser

# Instantiate client
auth_client = AuthClient(
    "ABcWQcMeUTm1r9Qq209oSi8ZIvTJ47HpKPqDF3tOOqHiPKicKN",
    "QX7rR2fWdE0TEZbqi537OOYpLiKiSPd4D05xTK4d",
    "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
    "sandbox",
)

# Prepare scores
scopes = [
    Scopes.ACCOUNTING,
]

# Get auth URL
auth_url = auth_client.get_authorization_url( scopes )

print( auth_url )

webbrowser.open( auth_url, new=0, autoraise=True )

auth_code = input( "Please enter code: " )
realm_id = input( "Please enter realm id: " )

# Get oauth2 bearer token
auth_client.get_bearer_token( auth_code, realm_id=realm_id )

# retrieve access_token and refresh_token
access_token = auth_client.access_token
refresh_token = auth_client.refresh_token

print( "Access token:", access_token )
print( "Refresh token:", refresh_token )
