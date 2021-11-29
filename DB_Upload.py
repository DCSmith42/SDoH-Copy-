#import psycopg2
import sqlalchemy
import pandas as pd

# TableName is the name of the table that will be created in the database.
# Dataframe is the pandas dataframe that will be upload to the database.
# DB is the location of the database. example: postgresql://postgres:Password@localhost/DatabaseName
# Schema is the name of database schema that will be used.
def upload(TableName, Dataframe, DB, Schema):
    
    name = str(TableName)
    
    db = str(DB)
    
    sch = Schema
    
    # Read in dataset (pandas format).
    df = Dataframe

    # Connects to data base.
    engine = sqlalchemy.create_engine(db)
    con = engine.connect()

    # Adds table to data base.
    df.to_sql(name, con, schema=sch, if_exists='replace')

    con.close()
    
    return 1
