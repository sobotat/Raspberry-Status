import re
from datetime import datetime, timedelta
import subprocess

class SSHApi:

    def getUsers(self, output:str = None):
        if output == None:
            try:
                output = subprocess.run(['who', '-u'], capture_output=True, text=True).stdout
            except Exception:
                print('Failed to read output from "who -u"')
                return []

        pattern = re.compile(r'(\S+)\s+(\S+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+(\d+:\d+|\.)\s+(\d+)\s+\((.+)\)')

        out = []

        for line in output.split('\n'):
            match = pattern.match(line)
            if match:
                username, terminal, login_time_str, idle_time_str, process_id, ip_address = match.groups()

                # Convert login time to datetime object
                login_time = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M")

                # Convert idle time to timedelta object
                if idle_time_str != '.':
                    idle_minutes = int(idle_time_str.split(':')[0]) * 60 + int(idle_time_str.split(':')[1])
                    idle_time = timedelta(minutes=idle_minutes)
                else:
                    idle_time = None

                user = {
                    'username': username,
                    'terminal': terminal,
                    'login-time': login_time,
                    'idle-time': idle_time,
                    'process-id': process_id,
                    'ip-address': ip_address,
                }

                out.append(user)

        return out

    def getActiveUsers(self, users:list, distinctUsers:bool = False, maxIdleMinutes:int = 5):
        out = []
        usedUsers = []

        for user in users:
            if type(user) is dict:
                if user['username'] in usedUsers and distinctUsers:
                    continue
                        
                idle:timedelta = user['idle-time']
                if idle != None and idle.total_seconds() > 60 * maxIdleMinutes:
                    continue

                out.append(user)

                if distinctUsers:
                    usedUsers.append(user['username'])

        return out
