import ftplib
import os
from traceback import format_exc
from datetime import datetime
import time
from pyrogram import Client
import keyring
import paramiko
        
def send_telegram_dmz(status):
    api_id =  'api_hash'
    api_hash = "api_hash"
    with Client("my_account", api_id, api_hash) as app:
        if status == True:
            app.send_message("tele_id", "Get DMZ backup database successful.")
        else:
            app.send_message("tele_id", "Error Get DMZ backup database!!!")

def main():
    filename=str(datetime.now()).split(' ')[0]+".bak"
    commands=[
        f"runuser -l postgres -c 'pg_dumpall > {filename}'",
    ]
    print('Create backup and transfer ...')
    for cmd in commands:
        tt=0
        time.sleep(5)
        for hdjsghdj in range(10):
            try:
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('psql_ip_add', username='root', password=keyring.get_password("pass_psql","root"))
                stdin, stdout, stderr = ssh.exec_command(cmd)
                for line in stdout:
                    print('... ' + line.strip('\n'))
                error=stderr.readlines()
                if len(error)>0:
                    print('stderr:',error)
                else:
                    tt=1
                    break
            except Exception as e:
                print(e)
                ssh.close()
        if tt==0:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            for line in stdout:
                print('... ' + line.strip('\n'))
            error=stderr.readlines()
        ssh.close()

    print('Created backup and transfered.')
    with ftplib.FTP('#ftp_add') as ftp:
        ftp.login('ftp_user', 'ftp_pass')
        print('File uploading ...')
        with open(f'/psql/backups/{filename}', 'rb') as fp:
            res = ftp.storbinary("STOR " + filename, fp)
        print('Uploaded successful.')
        send_telegram_dmz(True)
     
main()
