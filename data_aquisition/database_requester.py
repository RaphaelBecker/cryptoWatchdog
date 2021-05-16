# #%% <-  Delete # for scientific mode!
import pandas as pd
import psycopg2
import math
import datetime
from sqlalchemy import create_engine

db_password = 'qwertyuiopasdfghjklzxcvbnm'
# db_password = os.environ.get('DB_PASSWORD')  # Set to your own password
db_name = 'crypto_currency_test_database'
# Create a database connection
engine = create_engine('postgresql://postgres:{}@localhost/{}'.format(db_password, db_name))


# returns a dataframe with every n record for a symbol
def get_every_nth_record_as_dataframe(n, symbol):
    every_nth_record_dataframe_query = 'SELECT * FROM (SELECT *, row_number() over() "rn" FROM "' + symbol + '") foo WHERE foo.rn %% ' + str(n) + ' = 0;'
    every_nth_record_dataframe = pd.read_sql_query(every_nth_record_dataframe_query, engine)
    return every_nth_record_dataframe


# returns a dataframe with every n price for a symbol
def get_every_nth_price_as_dataframe(frequency, update_time, coin_name):
    now = datetime.datetime.now()
    start = now - datetime.timedelta(seconds=update_time*frequency)
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    # TODO: In actual implementation this needs to be deleted
    # print(start, now)
    start = '2021-04-02 18:10:22'
    now = '2021-04-16 18:10:22'
    # Important SQL query to query data from selected dates
    every_nth_price_dataframe_query = \
        'SELECT * FROM crypto_master_data ' \
        'WHERE time_stamp < \'{}\' ' \
        'AND crypto_master_data.time_stamp > \'{}\' ' \
        'AND crypto_master_data.base = \'{}\';'.format(now, start, coin_name)

    every_nth_price_dataframe = pd.read_sql_query(every_nth_price_dataframe_query, engine)
    # Database must not be empty
    assert len(every_nth_price_dataframe) > 0, 'Data base is empty'
    every_nth_price_dataframe = every_nth_price_dataframe[every_nth_price_dataframe.index % (math.ceil(len(every_nth_price_dataframe) / frequency)) == 0]
    print(every_nth_price_dataframe)

    # every_nth_price_dataframe_query = 'SELECT * FROM crypto_master_data WHERE time_stamp < \'2021-03-30 00:00:00\' AND crypto_master_data.time_stamp > \'2021-03-28 00:00:00\' AND crypto_master_data.base = \'Bitcoin\';'
    # every_nth_price_dataframe_query = 'SELECT "Price" FROM (SELECT *, row_number() over() "rn" FROM "' + symbol + '") foo WHERE foo.rn %% ' + str(n) + ' = 0;'
    # every_nth_price_dataframe = pd.read_sql_query(every_nth_price_dataframe_query, engine)
    # return every_nth_price_dataframe
