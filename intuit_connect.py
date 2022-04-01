from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from google.cloud import bigquery
import webbrowser
import json
import os

company_id = '9130352109852406'

bq_client = bigquery.Client()

query_job = bq_client.query(
    f"""
    SELECT *
    FROM `yetibooks-reporting.Utility.QBO_Secret_Store`
    WHERE company_id = '{ company_id }'
    """
)

results = query_job.result()

for row in results :

    client_id = row.client_id
    client_secret = row.client_secret
    redirect_uri = row.redirect_url
    environment = row.environment

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

update_job = bq_client.query(
    f"""
    Update`yetibooks-reporting.Utility.QBO_Secret_Store`
        set access_token = '{ access_token }'
           ,refresh_token = '{ refresh_token }'
    where company_id = '{ company_id }'
    """
)

result = update_job.result()
