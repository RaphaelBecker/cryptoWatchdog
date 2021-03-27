#!/usr/bin/env python3
import time
from sqlalchemy import create_engine
from data_aquisition.requester import get_binance_data
import pandas as pd


def store_to_db():
    """
    Store data from the binance API to the postgres Database.
    :return: void
    """
    i = 0
    while True:
        # Updates every <update_time> seconds
        update_time = 5
        i += 1
        print("Running...", i)
        # Get data from the binance API as a dataframe
        data = get_binance_data()
        db_password = 'qwertyuiopasdfghjklzxcvbnm' # Store in env vars
        db_name = 'crypto_currency'
        engine = create_engine(('postgresql://postgres:{}@localhost/'+db_name).format(db_password))
        # Write to database
        if engine.dialect.has_table(engine, 'crypto_master_data'): # Check if database table already exists
            data.to_sql('crypto_master_data', engine, if_exists='append', index=False)
        else:
            data.to_sql('crypto_master_data', engine, if_exists='append', index=False)
            query = """ALTER TABLE crypto_master_data
                        ADD PRIMARY KEY (base, time_stamp);"""
            engine.execute(query)

        time.sleep(update_time)


if __name__ == "__main__":
    store_to_db()
