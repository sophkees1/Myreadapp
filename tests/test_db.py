import unittest
import re
from src.database import Database


# we want to test for singleton
# we want to test for database connectivity

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = Database()
        
    # singleton test
    def test_singleton(self):
        connection1 = Database()
        connection2 = Database()
        
        self.assertEqual(connection1, connection2)
    
    # test connection, should have in all tests with databases   
    def test_postgres_version(self):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT version();') # execute sql statement
            db_version = cursor.fetchone()[0] # get one row, [0] gets first object in tuple(row)
            self.assertRegex(db_version, r'^(PostgreSQL 15.3)')
            
               
    def tearDown(self) -> None:
        self.conn.close()
        