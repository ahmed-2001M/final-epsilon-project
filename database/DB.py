import psycopg2

class PostgreSQLConnection:
    def __init__(self, host = "172.17.0.2", database = "work", user = "postgres", password = "123"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connected to the PostgreSQL database")

        except psycopg2.Error as e:
            print(f"Error connecting to the PostgreSQL database: {e}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Connection to PostgreSQL closed")



    def execute_query(self, query, values=None):
        try:
            if self.connection and self.cursor:
                self.cursor.execute(query, values)
                return self.cursor.fetchall()
            else:
                
                print("Not connected to the database. Call 'connect' method first.")
                return None

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None


    def execute_insert(self, query, data):
        try:
            if self.connection and self.cursor:
                for row in data:
                    self.cursor.execute(query, row)
                    self.connection.commit()
                    print("Row inserted successfully.")
            else:
                print("Not connected to the database. Call 'connect' method first.")
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error executing individual inserts: {e}")

    def execute_batch_insert(self, query, data):
        try:
            if self.connection and self.cursor:
                self.cursor.executemany(query, data)
                self.connection.commit()
                print(f"{self.cursor.rowcount} rows inserted successfully.")
            else:
                print("Not connected to the database. Call 'connect' method first.")
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error executing batch insert: {e}")



