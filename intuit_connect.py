from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import webbrowser
import json

config_file_path = "./config.json"

with open( config_file_path ) as config_f :
    config_data = json.load( config_f )

client_id = config_data[ 'client_id' ]
client_secret = config_data[ 'client_secret' ]
redirect_uri = config_data[ 'redirect_uri' ]
environment = config_data[ 'environment' ]

# Instantiate client
auth_client = AuthClient( client_id = client_id,
                          client_secret = client_secret,
                          redirect_uri = redirect_uri,
                          environment = environment )

# Prepare scores
scopes = [ Scopes.ACCOUNTING ]

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

config_data[ 'access_token' ] = access_token
config_data[ 'refresh_token' ] = refresh_token

with open( config_file_path, 'w' ) as config_f :
    json.dump( config_data, config_f )

