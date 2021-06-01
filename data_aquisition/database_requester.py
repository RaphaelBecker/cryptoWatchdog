# #%% <-  Delete # for scientific mode!
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine

#TODO: replace for production: password, db_name
db_password = ''
# db_password = os.environ.get('DB_PASSWORD')  # Set to your own password
#db_name = 'CryptoCurrencyDataBase'
db_name = 'raphael'
# Create a database connection
engine = create_engine('postgresql://postgres:{}@localhost/{}'.format(db_password, db_name))

# returns a dataframe with every n record for a symbol
def get_every_nth_record_as_dataframe(n, symbol):
    every_nth_record_dataframe_query = 'SELECT * FROM (SELECT *, row_number() over() "rn" FROM "' + symbol + '") foo WHERE foo.rn %% ' + str(
        n) + ' = 0;'
    every_nth_record_dataframe = pd.read_sql_query(every_nth_record_dataframe_query, engine)
    return every_nth_record_dataframe


# returns a dataframe with every n price for a symbol
def get_every_nth_price_as_dataframe(n, symbol):
    every_nth_price_dataframe_query = 'SELECT "Price" FROM (SELECT *, row_number() over() "rn" FROM "' + symbol + '") foo WHERE foo.rn %% ' + str(
        n) + ' = 0;'
    every_nth_price_dataframe = pd.read_sql_query(every_nth_price_dataframe_query, engine)
    return every_nth_price_dataframe


# returns the whole database as a dataframe
def get_db_as_dataframe():
    whole_database_query = 'SELECT * FROM crypto_master_data;'
    whole_database_dataframe = pd.read_sql_query(whole_database_query, engine)
    return whole_database_dataframe
