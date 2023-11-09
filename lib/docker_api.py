from lib.database import Database
from datetime import datetime
try:
    import docker
except ImportError:
    print('Install Docker pip install docker')

class DockerApi:
    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DockerApi, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if DockerApi.__instance is None:
            self.client = docker.DockerClient()

    def getContainersData(self):
        list = self.client.containers.list(all=True)
        out = []
        for container in list:
            if len(container.image.tags) == 0: continue
            name = container.image.tags[0]
            out.append({
                'container-name': container.name, 
                'image-name':name, 
                'status':container.status
            })
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
                if container['image-name'] == name:
                    using += 1
                    active += (1 if container['status'] == 'running' else 0)

            out.append({
                'image-name': name, 
                'using': using, 
                'active': active
            })
        return out
    
    def sendContainersData(self):
        insert_query = "INSERT INTO docker_containers_data (time, count, active) VALUES (%s, %s, %s)"
        
        database = Database()
        date = datetime.now()
        list = self.getContainersData()
        count = 0
        active = 0

        for container in list:
            active += 1 if container['status'] == 'running' else 0
            count += 1

        database.send(insert_query, (date, count, active))
        
            