from vmwc import VMWareClient
import keyring
from pyrogram import Client

hosts = [
    [
        "Your_host_ip",
        'user',
        keyring.get_password("pass_host1","user"),
        []
    ],
    [
        "Your_host_ip",
        'user',
        keyring.get_password("pass_host2", "user"),
        []
    ],
    [
        "Your_host_ip",
        'user',
        keyring.get_password("pass_host3", 'user'),
        []
    ]
]

def send_telegram(text):
    api_id =  'api_id'
    api_hash = "api_hash"

    with Client("my_account", api_id, api_hash) as app:
        app.send_message("Your_tele_id", text)
cc=0
for h in hosts:
    cc+=1
    try:
        with VMWareClient(h[0], h[1], h[2]) as client:
            for vm in client.get_virtual_machines():
                if vm.is_powered_off():
                    print(vm.name,vm.is_powered_off())
                    if vm.is_powered_off() == True and vm.name not in h[3]:
                        text=f"host: {cc} server: {vm.name} is off"
                        send_telegram(text)
    except Exception as e:
        text=f'!!! Error code !!!\nhost: {cc}\nError: {str(e)}'
        send_telegram(text)
