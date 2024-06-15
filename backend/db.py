import psycopg2
from config import db_config

def connect_db():
    connection = psycopg2.connect(**db_config)
    return connection

def create_user_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(250) NOT NULL,
        sessionid VARCHAR(250) NOT NULL
    )             
''')
    
    conn.commit()
    cursor.close()
    conn.close()
    