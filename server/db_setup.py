import pandas as pd
import urllib.request
import lzma
from pathlib import Path

def setup(engine):
    #check if bus data exists
    table_name = 'bus'
    query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"

    table_exists = pd.read_sql(query, engine)

    if table_exists.iloc[0, 0]:
        print('table already exists')
    else:
        print('table does not exist, downloading files...')
        urllib.request.urlretrieve('https://s3.amazonaws.com/nycbuspositions/2023/05/2023-05-14-bus-positions.csv.xz', '2023-05-14-bus-positions.csv.xz')
        with lzma.open("2023-05-14-bus-positions.csv.xz") as f, open('2023-05-14-bus-positions.csv', 'wb') as fout:
            file_content = f.read()
            fout.write(file_content)

        print('writing to database')
        df = pd.read_csv('./2023-05-14-bus-positions.csv.xz')
        df.to_sql('bus', con=engine, if_exists='append')

        #clean up 
        for p in Path(".").glob("*bus-positions.csv*"):
            p.unlink()
