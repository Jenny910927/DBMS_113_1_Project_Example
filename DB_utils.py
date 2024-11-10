import sys
import psycopg2


DB_NAME = "STUDY_GROUP"
DB_USER = "DBTA"
DB_HOST = "127.0.0.1"
DB_PORT = 5432



def db_connect():
    exit_code = 0
    db = None
    try:
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='1234', 
                              host=DB_HOST, port=DB_PORT)
        # exit_code = main(db)
        print("Successfully connect to DBMS.")
        return db
        
    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    # finally:
    #     if db is not None:
    #         db.close()
    sys.exit(exit_code)
    

def fetch_data(db, cmd):
    cur = db.cursor()

    if cmd == "test":
        cur.execute('select * from test;')

        for tup in cur.fetchall():
            print(f'fetch: {tup}')