# from psycopg2 import connect, cursor
from psycopg2.extras import RealDictCursor
import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(host="localhost", database="Learning-API-Dev", user="postgres", password="123", cursor_factory=RealDictCursor)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute('SELECT * FROM public."Product"')

# Retrieve query results
records = cur.fetchall()