# from psycopg2 import connect, cursor
from psycopg2.extras import RealDictCursor
import psycopg2
from time import sleep


# Connect to your postgres DB
try :
    conn = psycopg2.connect(host="localhost", database="Learning-API-dev", user="postgres", password="123", cursor_factory=RealDictCursor)
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute('SELECT * FROM public."Product" ; ')

    # Retrieve query results
    records = cur.fetchall()
    print(records)


except Exception as error_var :
    print("Failed to connect to DB ...")
    print("Error :- \n ", error_var)

    
    
    
# MUCH BETTER WAY TO DO THIS :-
while True:
    try :
        # conn = psycopg2.connect(host="localhost", database="Learning-API-dev", user="postgres", password="123", cursor_factory=RealDictCursor)

        conn = psycopg2.connect(host="localhost", database="Learning-API-dev", user="postgres", password="123", cursor_factory=RealDictCursor)  
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."Product" ; ')
        records = cur.fetchall()
        print(records)
        break  # the only way for this loop to end is if IT SUCCESSFULLY CONNECTS to the db
    
    except Exception as error_var :
        print("Failed to connect to DB ...")
        print("Error :- \n ", error_var)
        
        sleep(2)  # 2 seconds()

    