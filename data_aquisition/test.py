# %%
import time
from data_aquisition.database_updater import process_symbols
from data_aquisition.database_updater import delete_all_tables
from data_aquisition.database_requester import get_every_nth_price_as_dataframe
import pandas as pd


def test():

    delete_all_tables()
    time.sleep(2)
    process_symbols()
    time.sleep(2)

    print(get_every_nth_price_as_dataframe(2, 'Bitcoin_data'))
    print(get_every_nth_price_as_dataframe(2, 'Cardano_data'))


# delete_all_tables()
# time.sleep(2)
# process_symbols()


test()

