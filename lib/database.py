try:
    import psycopg2
except ImportError:
    print("Install Postgres pip install psycopg2-binary")
from lib.logger import Logger, Level

class Database:
    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if Database.__instance is None:
            Database.__instance = self
            self.logger = Logger('Database')
            self.connection = None
            self.cursor = None
            self.initDB()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

    def initDB(self) -> bool:
        table_raspberry_data = '''
            CREATE TABLE IF NOT EXISTS raspberry_data (
                time TIMESTAMP PRIMARY KEY,
                cpu FLOAT NOT NULL,
                temp FLOAT NOT NULL,
                upload FLOAT NOT NULL,
                download FLOAT NOT NULL,
                memory FLOAT NOT NULL,
                active_ssh FLOAT NOT NULL
            );
            '''
        table_docker_containers_data = '''
            CREATE TABLE IF NOT EXISTS docker_containers_data (
                time TIMESTAMP PRIMARY KEY,
                count FLOAT NOT NULL,
                active FLOAT NOT NULL
            );
            '''
        
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                port=5400,
                database="grafana_db",
                user="grafana",
                password="grafana")

            self.cursor = self.connection.cursor()
            self.cursor.execute(table_raspberry_data)
            self.cursor.execute(table_docker_containers_data)
            self.connection.commit()
            self.logger.log(Level.Info, "DB was Init")
            return True
        except Exception:
            self.connection = None
            self.cursor = None
            self.logger.log(Level.Error, "Failed to Init DB")
            return False

    def send(self, query:str, parameters:tuple = ()):
        if self.connection == None:
            if not self.initDB():
                self.logger.log(Level.Error, "Failed to send quary to DB -> Not Init")
                return
        try:
            if parameters == ():
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, parameters)
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")