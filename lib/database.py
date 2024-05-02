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
            self.wasInit = False
            self.initDB()

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
            connection, cursor = self.getConnection()
            cursor.execute(table_raspberry_data)
            cursor.execute(table_docker_containers_data)
            connection.commit()
            connection.close()
            self.wasInit = True
            self.logger.log(Level.Info, "DB was Init")
            return True
        except Exception:
            self.logger.log(Level.Error, "Failed to Init DB")
            return False

    def send(self, query:str, parameters:tuple = ()):
        if not self.wasInit:
            if not self.initDB():
                self.logger.log(Level.Error, "Failed to send quary to DB -> Not Init")
                return
        try:
            connection, cursor = self.getConnection()
            if parameters == ():
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            connection.commit()
            connection.close()
        except Exception as e:
            self.logger.log(Level.Error, f"Send Failed: {e}")

    def getConnection(self):
        connection = psycopg2.connect(
                host="localhost",
                port=5400,
                database="grafana_db",
                user="grafana",
                password="grafana")

        cursor = connection.cursor()
        return connection, cursor