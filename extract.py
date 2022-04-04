from flask import Flask, request
from intuitlib.client import AuthClient
from google.cloud import bigquery
from google.cloud.bigquery import Client
from google.cloud import storage
from google.cloud.storage import blob
from quickbooks import QuickBooks
from quickbooks.objects import Customer
from parse import parse_data
import json
import csv
import os
import datetime

app = Flask( __name__ )

def initialize_clients( company_id: str ) -> tuple[ QuickBooks, Client ] :
    """Initializes the QuickBooks and BigQuery Clients

    Args :
        company_id (str) : company to pull secrets for

    Returns :
        QuickBooks : quickbooks client
        Client : bigquery client
    """

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
        access_token = row.access_token
        environment = row.environment
        redirect_uri = row.redirect_url
        refresh_token = row.refresh_token
    
    # Instantiate auth client
    auth_client = AuthClient(
        client_id = client_id,
        client_secret = client_secret,
        access_token = access_token,
        environment = environment,
        redirect_uri = redirect_uri,
    )
    
    # Instantiate client
    qb_client = QuickBooks(
        auth_client = auth_client,
        refresh_token = refresh_token,
        company_id = company_id,
    )

    return qb_client, bq_client

def insert_data( bq_client: Client, filename: str ) -> str :
    """Insert/Appends data to a BQ table

    Args: 
        bq_client (Client) : client to make api calls to
        filename (str) : local file to insert into BQ table

    Returns :
        str : 'ok' response
    """

    table_id = 'yetibooks-reporting.qbo_raw.customers'

    job_config = bigquery.LoadJobConfig(
        schema = [ bigquery.SchemaField( 'id', 'INT64' ),
                   bigquery.SchemaField( 'company_id', 'INT64' ),
                   bigquery.SchemaField( 'rowloadeddatetime', 'TIMESTAMP' ),
                   bigquery.SchemaField( 'payload', 'STRING' ) ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format = bigquery.SourceFormat.CSV,
    )

    with open( filename, 'rb' ) as f :
        
        load_job = bq_client.load_table_from_file( f,
                                                   table_id,
                                                   job_config = job_config )

        load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table( table_id )
    print( f'Loaded { destination_table.num_rows } rows.' )

    return 'ok'

@app.route( '/' )
def extract_data() :
    """Driver code for the extract QuickBooksOnline extract
    """
    
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
        access_token = row.access_token
        environment = row.environment
        redirect_uri = row.redirect_url
        refresh_token = row.refresh_token
    
    # Instantiate auth client
    auth_client = AuthClient(
        client_id = client_id,
        client_secret = client_secret,
        access_token = access_token,
        environment = environment,
        redirect_uri = redirect_uri,
    )
    
    # Instantiate client
    qb_client = QuickBooks(
        auth_client = auth_client,
        refresh_token = refresh_token,
        company_id = company_id,
    )
    
    customers = Customer.all( qb=qb_client )

    parse_data( customers, 'customer.csv' )

    return 'ok', 200

if __name__ == "__main__" :

    app.run( host='0.0.0.0', port=int( os.getenv( 'PORT', 8080 )))

