# #%% <-  Delete # for scientific mode!
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine

db_password = 'password'
# db_password = os.environ.get('DB_PASSWORD')  # Set to your own password
db_name = 'CryptoCurrencyDataBase'
# Create a database connection
engine = create_engine('postgresql://postgres:{}@localhost/{}'.format(db_password, db_name))


# returns a dataframe with every n record for a symbol
def get_every_nth_record_as_dataframe(n, symbol):
    every_nth_record_dataframe_query = 'SELECT * FROM (SELECT *, row_number() over() "rn" FROM "' + symbol + '") foo WHERE foo.rn %% ' + str(n) + ' = 0;'
    every_nth_record_dataframe = pd.read_sql_query(every_nth_record_dataframe_query, engine)
    return every_nth_record_dataframe


# returns a dataframe with every n price for a symbol
def get_every_nth_price_as_dataframe(n, symbol):
    every_nth_price_dataframe_query = 'SELECT "Price" FROM (SELECT *, row_number() over() "rn" FROM "' + symbol + '") foo WHERE foo.rn %% ' + str(n) + ' = 0;'
    every_nth_price_dataframe = pd.read_sql_query(every_nth_price_dataframe_query, engine)
    return every_nth_price_dataframe
