import docker
from lib.database import Database
from datetime import datetime

class Docker:
    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Docker, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if Docker.__instance is None:
            self.client = docker.from_env()

    def getContainersData(self):
        list = self.client.containers.list(all=True)
        out = []
        for container in list:
            if len(container.image.tags) == 0: continue
            name = container.image.tags[0]
            out.append((container.id, name, container.status))
        return out
    
    def getImagesData(self):
        list = self.client.images.list(all=True)
        containers = self.getContainersData()
        out = []
        for image in list:
            using = 0
            active = 0
            if len(image.tags) == 0: continue
            name = image.tags[0]
            for container in containers:
                if container[1] == name:
                    using += 1
                    active += (1 if container[2] == 'running' else 0)

            out.append((name, using, active))
        return out
    
    def sendContainersData(self):
        insert_query = "INSERT INTO docker_containers_data (name, image, is_running, time) VALUES (%s, %s, %s, %s)"
        
        database = Database()
        date = datetime.now()
        list = self.getContainersData()

        for container in list:
            database.send(insert_query, (container[0], container[1], container[2] == 'running', date))