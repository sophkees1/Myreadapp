import psycopg as pg
import environ
from typing import Optional, Union
from datetime import date
from tabulate import tabulate
from src.schema import CreateDataType, FetchByIdDataType
from src.util import ROOT_DIR

# CREATE A CONNECTION

env = environ.Env()
# /home/..../myreadapp/.env
# Set .env from the root dir to be read
environ.Env.read_env(str(ROOT_DIR / '.env'))



# SINGLETON CLASS
class Database(object):
    _instance = None
    
    def __new__(cls):
        if Database._instance is None:
            Database._instance = super().__new__(cls)
            Database._instance.__init__()
            
        return Database._instance._conn
    
    def __init__(self) -> None:
        # connects to postgres server
        # it is bad practice to reveal sensitive information in your code
        self._conn = pg.connect(
            host=env.str('db_host'),
            dbname=env.str('db_name'),
            user=env.str('db_user'),
            password=env.str('db_password'),
            port=env.int('db_port')
        )


def insert_data(data: CreateDataType) -> None:
    # get the connection
    conn = Database()
    # define the query
    query = """
            INSERT INTO read.bookclub(
                username,
                title,
                description,
                status,
                pct_read,
                start_read_date,
                end_read_date               
            ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;           
    """
    # create the cursor session
    with conn.cursor() as cursor:
        # use the cursor session to execute the query
        cursor.execute(query, tuple(data.values()))
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        return inserted_id
   
    
def fetch_by_id(book_id: int) -> Optional[FetchByIdDataType]:
    conn = Database()
    query = """
            SELECT
                title,
                description,
                status,
                pct_read,
                start_read_date,
                end_read_date
            FROM read.bookclub
            WHERE id=%s;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()
        return book

def update_data(
    book_id: int, column: str, data: Union[str, date, int]
) -> Optional[int]:
    conn = Database()
    query = """
        UPDATE read.bookclub
        SET """+ column +"""=%s
        WHERE id=%s RETURNING id;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, [data, book_id])
        updated_book_id = cursor.fetchone()[0]
        conn.commit()
        return updated_book_id
    
def delete_row(book_id: int) -> Optional[int]:
    conn = Database()
    query = """
        DELETE FROM read.bookclub
        WHERE id=%s
        RETURNING id; 
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (book_id,))
        deleted_book_id = cursor.fetchone()[0]
        conn.commit()
        return deleted_book_id
        
def truncate_table():
    conn = Database()
    query = """
        TRUNCATE TABLE read.bookclub RESTART IDENTITY;   
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
        
def view_table():
    conn = Database()
    query = """
        SELECT * FROM read.bookclub
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        table = tabulate(rows, headers=column_names, tablefmt='fancy_grid')
        print(table)
        
def count_completed_books(start_date, end_date):
    conn = Database()
    query1 = """
        SELECT * FROM read.bookclub
        WHERE status = 'complete';
        """
    query2 = f"""
        SELECT COUNT(*)
        FROM read.bookclub 
        WHERE status = 'complete' 
        AND start_read_date >= '{start_date}' 
        AND end_read_date <= '{end_date};'
        """
    with conn.cursor() as cursor:
        cursor.execute(query1)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        table = tabulate(rows, headers=column_names, tablefmt='fancy_grid')
        print(table)
    
    with conn.cursor() as cursor:
        cursor.execute(query2)
        count = cursor.fetchone()[0]
        return count
 
   
def count_pending_books():
    conn = Database()
    query1 = """
        SELECT * FROM read.bookclub
        WHERE status = 'pending';
        """
    query2 = """
        SELECT COUNT(*) FROM read.bookclub 
        WHERE status = 'pending';
        """
    with conn.cursor() as cursor:
        cursor.execute(query1)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        table = tabulate(rows, headers=column_names, tablefmt='fancy_grid')
        print(table)
        
    with conn.cursor() as cursor:       
        cursor.execute(query2)
        count = cursor.fetchone()[0]
        return count
 
def search_books_by_title(title):
    conn = Database()
    query = f"""
    SELECT * FROM read.bookclub
    WHERE title ILIKE '%{title}%';
    """
    with conn.cursor() as cursor:    
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        table = tabulate(rows, headers=column_names, tablefmt='fancy_grid')
        print(table)
    