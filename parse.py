"""Contains functions to parse QuickBooksOnline data types
"""

import json
import csv
import datetime

def flattenjson( i_item: dict, delim: str, line_list: list ) :

    val = {}
    for i_key in i_item.keys() :

        if isinstance( i_item[ i_key ], list ) \
                and i_key == 'Line' :

            for line_item in i_item[ i_key ] :

                new_val = {}
                j_item, _ = flattenjson( line_item, delim, line_list )

                for j_key in j_item.keys() :
                
                    new_val[ i_key + delim + j_key ] = j_item[ j_key ]
                
                line_list.append( new_val )

        if isinstance( i_item[ i_key ], list ) \
                and len( i_item[ i_key ] )  == 1 \
                and i_key != 'Line' :

            j_item, _ = flattenjson( i_item[ i_key ][0], delim, line_list )
            for j_key in j_item.keys() :

                val[ i_key + delim + j_key ] = j_item[ j_key ]
                
        if isinstance( i_item[ i_key ], dict ) :

            j_item, _ = flattenjson( i_item[ i_key ], delim, line_list )
            for j_key in j_item.keys() :

                val[ i_key + delim + j_key ] = j_item[ j_key ]

        else :
            val[ i_key ] = i_item[ i_key ]

    return val, line_list

def parse_data( data, blobname, company_id ) :
    """Given a QuickBooks json iterable object,
    parse the data and save to blobname
    
    Args :
        data ( ) : data to translate
        blobname (str) : location to save csv to
        parse_func (function) : function to parse json obj

    Return :
        str : location csv was saved to

    """

    print( '[TRANSLATE] - Translating json data into csv file' )

    new_data = []
    new_line_data = []
    for row in data :
        row = row.to_json()
        row = json.loads( row )
        
        row['company_id'] = company_id
        row['rowloadeddatetime'] = datetime.datetime.today()

        row, line_list = flattenjson( row, '_', [] )

        for line_item in line_list :
            line_item['Id'] = row['Id']
            
            new_line_data.append( line_item )

        new_data.append( row )
    
    data = new_data

    columns = [ x for row in data for x in row.keys() ]
    columns = list( set( columns ) )

    with open( blobname, 'w' ) as out_f :

        writer = csv.writer( out_f )
        writer.writerow( columns )

        for item in data :
            writer.writerow( map( lambda x: item.get( x, ""), columns ) )

    if len( new_line_data ) > 0 :
        print('dp o gt hee')

        data = new_line_data

        columns = [ x for row in data for x in row.keys() ]
        columns = list( set( columns ) )

        with open( blobname[:-4] + '_line.csv', 'w' ) as out_f :

            writer = csv.writer( out_f )
            writer.writerow( columns )

            for item in data :
                writer.writerow( map( lambda x: item.get( x, ""), columns ) )

    return blobname

