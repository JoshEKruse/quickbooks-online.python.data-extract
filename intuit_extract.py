from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects import Customer
import json

config_file_path = "./config.json"

with open( config_file_path ) as config_f :
    config_data = json.load( config_f )

client_id = config_data[ 'client_id' ]
client_secret = config_data[ 'client_secret' ]
access_token = config_data[ 'access_token' ]
environment = config_data[ 'environment' ]
redirect_uri = config_data[ 'redirect_uri' ]
refresh_token = config_data[ 'refresh_token' ]
company_id = config_data[ 'company_id' ]


auth_client = AuthClient(
    client_id = client_id,
    client_secret = client_secret,
    access_token = access_token,
    environment = environment,
    redirect_uri = redirect_uri,
)

client = QuickBooks(
    auth_client = auth_client,
    refresh_token = refresh_token,
    company_id = company_id,
)

customers = Customer.all( qb=client )

print( customers )
