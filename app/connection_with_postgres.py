# from psycopg2 import connect, cursor
from psycopg2.extras import RealDictCursor
import psycopg2


# Connect to your postgres DB
try :
    conn = psycopg2.connect(host="localhost", database="Learning-API-dev", user="postgres", password="123", cursor_factory=RealDictCursor)
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute('SELECT * FROM "Product" ; ')

    # Retrieve query results
    records = cur.fetchall()
    print(records)

    
except Exception as error_var :
    print("Failed to connect to DB ...")
    print("Error :- \n ", error_var)