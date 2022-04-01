#!/usr/bin/python3
import paramiko
import pymysql
import time

USER_RB = ''
PASS_RB = ''
RADIUS_USER = ""
RADIUS_PASS = ""
RADIUS_DB = ""
IP = ""
IPoldone = ""
IPNew = ""

class SSH:
    def __init__(self, ip, authUsername, autPassword, difinePort= 22):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(ip, difinePort, authUsername, autPassword)
            print("Auth OK")
        except Exception as e:
            print(e)
                     
    def execute(self):
        listCommand = [
            "sed -i 's/aaa.1.radius.auth.1.ip={}/aaa.1.radius.auth.1.ip={}/' /tmp/system.cfg".format(IPoldone, IPNew),
            "/usr/etc/rc.d/rc.softrestart save"
        ] 
        for command in listCommand:
            _, _, stderr = self.ssh.exec_command(command)
            time.sleep(0.5)
            if len(stderr.readlines()) != 0:
                print(stderr.readlines())
            else:
                print("OK")
        self.ssh.close()
        print("Finalizado...")
                
                
def main():
    
    connection = pymysql.connect(host=IP, user=RADIUS_USER, password=RADIUS_PASS, database=RADIUS_DB)
    caunt = 0
    with connection:
        with connection.cursor() as cursor:
      
            sql = ""
            cursor.execute(sql)
       
            result = cursor.fetchone()
            while result is not None:
                caunt = caunt + 1
                print("IP: {} Base {} Processando...".format(result[1], result[2]))
                try:
            
                    ssh = SSH(result[1], "user", "pass", 22) 
                    ssh.execute()
                except Exception as e:
                    print("FALHA {}".format(e))
             
                result = cursor.fetchone()
            cursor.close()
            print(caunt)
                 
    


if __name__ == '__main__':
    	main()
