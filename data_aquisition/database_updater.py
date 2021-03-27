# #%% <-  Delete # for scientific mode!
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine

# TODO create password for database and implement PW as env var
db_password = 'password'
# db_password = os.environ.get('DB_PASSWORD')  # Set to your own password
db_name = 'CryptoCurrencyDataBase'
# Create a database connection
engine = create_engine('postgresql://postgres:{}@localhost/{}'.format(db_password, db_name))
bars_path = './data/runtime_coin_price_data'


# Create a SQL table directly from a dataframe df and symbol
def create_prices_table(symbol, df):
    # Insert new Collumn "updated" to indicate when the new records where added to the database
    df.insert(0, "Updated", True)
    df['Updated'] = pd.to_datetime('now')
    # Fill all NaN with 0 for a clean data set
    df = df.fillna(0)
    # Write the data into the database:
    df.to_sql(symbol, engine, if_exists='replace', index=False)
    return 'table created'


# This function will upsert (update/insert) new records into the existing symbol tables from dataframe df
def import_bar_file(symbol, df):
    # path to csv files which are going to be upsert into the database
    path = bars_path + '/{}.csv'.format(symbol)
    # Check if new price data is available: Latest TimeStamp in table earlier than latest timestamp in csv?
    latest_timestamp_query = 'SELECT "TimeStamp" FROM "' + symbol + '" ORDER BY "TimeStamp" DESC limit 1;'
    latest_timestamp_db = pd.read_sql_query(latest_timestamp_query, engine)
    # extract Timestamp from dataframes
    latest_timestamp_db = max(latest_timestamp_db['TimeStamp'])
    earliest_timestamp_df = min(df['TimeStamp'])
    if latest_timestamp_db < earliest_timestamp_df:
        print(' # Earlier price data available. Will be imported into table: ' + symbol + ' now!')
        import_csv_file(symbol, df)
    else:
        print(' # Table ' + symbol + ' is up to date! Nothing to import.')


# Helper function for def import_bar_file(): Imports data from csv into an existing table
def import_csv_file(symbol, df):
    # Insert new column "updated" to indicate when the data was added to the database
    df.insert(0, "Updated", True)
    df['Updated'] = pd.to_datetime('now')
    # Fill all NaN with 0 for a clean data set
    df = df.fillna(0)
    # First part of the insert pSQL statement for one record
    insert_init = str("""INSERT INTO "{}"
                    ("Updated", "TimeStamp", "Coin Name", "Price", "Volume", "Gain", "Loss", "Average Gains", "Average Loss", "Relative Strength", "RSI")
                    VALUES""").format(symbol)
    # Add values for all days to the insert statement
    vals = ",".join(["""('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')""".format(
        row['Updated'],
        row['TimeStamp'],
        row['Coin Name'],
        row['Price'],
        row['Volume'],
        row['Gain'],
        row['Loss'],
        row['Average Gains'],
        row['Average Loss'],
        row['Relative Strength'],
        row['RSI'],
    ) for date, row in df.iterrows()])
    # Put together the query string
    query = insert_init + vals  # insert_end
    # Fire insert statement
    engine.execute(query)
    return 'import of csv files successful'


# Deletes the SCHEMA public. Will erase all tables! Only for testing
def delete_all_tables():
    engine.execute(str("""DROP SCHEMA public CASCADE; CREATE SCHEMA public;"""))
    print('SCHEMA public was deleted')
    print('SCHEMA public was created')
    print(' ')
    return 'all tables deleted'


# This function will loop through all the files in the directory located in bars_path and process the CSV files
def process_symbols():
    # #%%
    symbols = [s[:-4] for s in os.listdir(bars_path)]
    # Clean import data: Only price data should be imported to the database. Cleaning property: Name contains '_data'
    index = 0;
    for symbol in symbols:
        if not symbol.__contains__('_data'):
            symbols.pop(index)
        index = index + 1
    for symbol in symbols:
        # Checks if Table already exists in database, if not, create table
        existing_tables = pd.read_sql_query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'",
            engine)
        if not str(symbol) in str(existing_tables):
            df = pd.read_csv('{}/{}.csv'.format(bars_path, symbol))
            create_prices_table(symbol, df)
            print('Price table "' + symbol + '" does not exist. Table created!')
            del df
        else:
            print('Importing ' + db_name + ' from ' + bars_path + '/' + symbol + '.csv ... ')
            df = pd.read_csv('{}/{}.csv'.format(bars_path, symbol))
            import_bar_file(symbol, df)
            del df
    return 'Process symbols complete'
