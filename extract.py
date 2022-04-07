from flask import Flask, request
from intuitlib.client import AuthClient
from google.cloud import bigquery
from google.cloud.bigquery import Client
from google.cloud import storage
from google.cloud.storage import blob
from quickbooks import QuickBooks
from quickbooks import objects as qbobj
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

    print( '[WORKING] - Initializing clients for company:', company_id )

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

def insert_data( bq_client: Client, filename: str, data_obj_name: str ) -> str :
    """Insert/Appends data to a BQ table

    Args: 
        bq_client (Client) : client to make api calls to
        filename (str) : local file to insert into BQ table

    Returns :
        str : 'ok' response
    """

    print( '[INSERT] - Inserting data into big query table for data obj:', data_obj_name )

    table_id = f'yetibooks-reporting.qbo_raw.{ data_obj_name }'

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        allow_quoted_newlines=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format = bigquery.SourceFormat.CSV,
    )

    with open( filename, 'rb' ) as f :
        
        load_job = bq_client.load_table_from_file( f,
                                                   table_id,
                                                   job_config = job_config )

        load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table( table_id )
    print( f'[COMPLETE] - Loaded { destination_table.num_rows } rows.' )

    return 'ok'

def run_etl( qb_client, bq_client, company_id, data_obj_name, qb_data_obj
            ,line_trig=False) :
    
    print( '[WORKING - running etl for data obj:', data_obj_name )

    blobname = f'{ data_obj_name }.csv'

    data_objs = qb_data_obj.all( qb=qb_client )

    if line_trig :

        parse_data( data_objs, blobname, company_id )
        insert_data( bq_client, blobname, data_obj_name )
        insert_data( bq_client, blobname[:-4] + '_line.csv', data_obj_name + '_line' ) 

    else :
    
        parse_data( data_objs, blobname, company_id )
        insert_data( bq_client, blobname, data_obj_name )

    return 'ok'


@app.route( '/' )
def extract_data() :
    """Driver code for the extract QuickBooksOnline extract
    """
    
    company_id = '9130352109852406'

    print( '[WORKING] - Starting load for company:', company_id )
    
    qb_client, bq_client = initialize_clients( company_id )

    run_etl( qb_client, bq_client, company_id, 'invoice', qbobj.Invoice, line_trig=True )
    run_etl( qb_client, bq_client, company_id, 'account', qbobj.Account )
    run_etl( qb_client, bq_client, company_id, 'attachable', qbobj.Attachable )
    run_etl( qb_client, bq_client, company_id, 'companyinfo', qbobj.CompanyInfo )
    run_etl( qb_client, bq_client, company_id, 'customer', qbobj.Customer )
    run_etl( qb_client, bq_client, company_id, 'deposit', qbobj.Deposit )
    run_etl( qb_client, bq_client, company_id, 'invoice', qbobj.Invoice )
    run_etl( qb_client, bq_client, company_id, 'item', qbobj.Item )
    run_etl( qb_client, bq_client, company_id, 'journalentry', qbobj.JournalEntry )
    run_etl( qb_client, bq_client, company_id, 'payment', qbobj.Payment )
    run_etl( qb_client, bq_client, company_id, 'paymentmethod', qbobj.PaymentMethod )
    run_etl( qb_client, bq_client, company_id, 'purchase', qbobj.Purchase )
    run_etl( qb_client, bq_client, company_id, 'taxcode', qbobj.TaxCode )
    run_etl( qb_client, bq_client, company_id, 'term', qbobj.Term )
    run_etl( qb_client, bq_client, company_id, 'vendor', qbobj.Vendor )

    return 'ok', 200

if __name__ == "__main__" :

    app.run( host='0.0.0.0', port=int( os.getenv( 'PORT', 8080 )))

