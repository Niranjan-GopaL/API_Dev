# from psycopg2 import connect, cursor
from psycopg2.extras import RealDictCursor, connect 
from time import sleep


# Connect to your postgres DB
try :
    conn = connect(host="localhost", database="Learning-API-dev", user="postgres", password="123", cursor_factory=RealDictCursor)
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
        # conn = psycopg2.connect(host="localhost", database="Learning-API-dev", user="postgres", password="wrong_password", cursor_factory=RealDictCursor)

        # USE DOTENV and fill these data; you can have a; .env ; .env_for_development; .env_for_production; .env_for_testing
        conn = connect(
            host="localhost", 
            database="Learning-API-dev", 
            user="postgres", 
            password="123", 
            cursor_factory=RealDictCursor
        )  
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."Product" ; ')
        records = cur.fetchall()
        print(records)
        break  # the only way for this loop to end is if IT SUCCESSFULLY CONNECTS to the db
    
    except Exception as error_var :
        print("Failed to connect to DB ...")
        print("Error :- \n ", error_var)
        
        sleep(2)  # 2 seconds()

    