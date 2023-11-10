import unittest
import json
import mysql.connector
from classes.db_conn import DatabaseConnection  # Import your DatabaseConnection class from your module

with open('../config.json') as config_file:
    config = json.load(config_file)


class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        # Get a new connection for each test
        self.connection = DatabaseConnection(config).get_connection_to_db()

    def tearDown(self):
        # Close the connection after each test
        self.connection.close()

    def test_get_connection_to_db(self):
        # Test if the get_connection_to_db method returns a valid connection
        self.assertIsInstance(self.connection, mysql.connector.MySQLConnection)


if __name__ == '__main__':
    unittest.main()
