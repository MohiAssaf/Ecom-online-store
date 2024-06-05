import psycopg2
from config import db_config

def connect_db():
    connection = psycopg2.connect(**db_config)
    return connection