import os
import paramiko
from ftplib import FTP
from password_generator import PasswordGenerator

pwo = PasswordGenerator()
pwo.minlen = 13
pwo.maxlen = 13 
pwo.minuchars = 2
pwo.minlchars = 3 
pwo.minnumbers = 1 
pwo.minschars = 1 
passkey = pwo.generate()
passuser = pwo.generate()

def main(host,port,username,password,name): 
    command1 = [
            f"certificate add name={name} common-name={name} days-valid=3650 key-size=2048 key-usage=tls-client",
            f" certificate sign {name} name={name} ca=ca-certificate",
            f'certificate export-certificate {name} export-passphrase="{passkey}"',
            f'ppp secret add name={name} password="{passuser}" service=any profile=VPN ',
            f"tool fetch address=#ftp_address src-path=cert_export_{name}.key  user=#ftp_user password=ftp_passwd port=21 mode=ftp  upload=yes dst-path=cert_export_{name}.key",
            f"tool fetch address=#ftp_address src-path=cert_export_{name}.crt  user=#ftp_user password=ftp_passwd  port=21 mode=ftp  upload=yes dst-path=cert_export_{name}.crt"
                ]         
    with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            for command in command1:
                print(command,end='\r')
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.read()
                print(lines.decode(),end='\r')
                print(lines.decode(),end='\r')

def ftp_(ip_ftp,user,passwd,name):
    ftp = FTP(ip_ftp)
    ftp.login(user,passwd) 
    ca = ''
    crt = ''
    keys = ''
    def writeFile_ca(data_ca):
        global ca 
        ca = data_ca.decode()
    def writeFile_crt(data_crt):
        global crt
        crt = data_crt.decode()
    def writeFile_keys(data_keys):
        global keys
        keys = data_keys.decode()
    ftp.retrbinary('RETR cert_export_ca-certificate.crt', writeFile_ca)
    ftp.retrbinary(f'RETR cert_export_{name}.crt', writeFile_crt)
    ftp.retrbinary(f'RETR cert_export_{name}.key', writeFile_keys)
    with open(f'#directory\{name}.ovpn', 'w') as f:
        f.write(f'client' '\n' 
        'dev tun' '\n' 
        'proto tcp' '\n' 
        'remote ##ip_address #port' '\n'
        'resolv-retry infinite' '\n' 
        'nobind' '\n'
        'persist-key' '\n'
        'persist-tun' '\n'
        'remote-cert-tls server' '\n'
        'cipher AES-128-CBC' '\n'
        'auth SHA1' '\n'
        'auth-user-pass' '\n'
        'redirect-gateway def1' '\n'
        'verb 3' '\n'
        '<ca>' '\n'
        f'{ca}'
        '</ca>' '\n'
        '<cert>' '\n'
        f'{crt}' '\n'
        '</cert>' '\n'
        '<key>' '\n'
        f'{keys}' '\n'
        '</key>'
        )   
        f.close()
    file = open(f'#directory\{name}.ovpn', 'rb')
    ftp.storbinary(f'STOR {name}.ovpn', file)
    file.close()
    ftp.quit()
