import mysql.connector


class DatabaseConnection:
    def __init__(self, config):
        self.db_config = config['database']
        self.db_host = self.db_config['host']
        self.db_user = self.db_config['user']
        self.db_password = self.db_config['password']
        self.db_name = self.db_config['database_name']
        self.connection = None

    def get_connection_to_db(self):
        """Establish a connection to a MySQL database."""
        self.connection = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        return self.connection

    def conn_close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None  # Reset the connection attribute
