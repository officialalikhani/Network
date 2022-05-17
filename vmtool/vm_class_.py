from vmwc import VMWareClient
from vmtools import ova

class vmware:
    def __init__(self): 
        self.obj =VMWareClient('#Your-address', '#Your-user', '#Your-passwd', port=443, verify=False)
        self.host='#Your-address'
        self.user='#Your-user'
        self.password='#Your-passwd'
        self.port='443'
        self.verify='False'
        self.path_='#Your-path'
        self.datastore_name='#Your-datastore'

    def getvm(self):
        for i in self.obj.get_virtual_machines():
            aa=i.name
        return aa

    def liah(self):
        client_vm = self.obj
        for vm in client_vm.get_virtual_machines():
            if vm.is_powered_off():
                if vm.is_powered_off() == True :#offvm
                    print(vm.name)
        for vm in client_vm.get_virtual_machines():
            if vm.is_powered_on():
                if vm.is_powered_on() == True :
                    print(f"{vm.name} is on")

    def enable_ssh(self):
        service_id = 'TSM-SSH'
        a= self.obj.start_service(service_id)
        return a

    def disable_ssh(self):
        service_id = 'TSM-SSH'
        self.obj.stop_service(service_id)

    def get_physical_interfaces(self):
        esxi_host = self.obj._get_single_esxi_host()
        for pnic in esxi_host.config.network.pnic:
            yield pnic.device

    def createvm(self,name):
        os=input('centos7_64Guest or windows9_64Guest :')
        client=self.obj
        vm = client.new_virtual_machine(name, remove_existing=False, 
        cpus=1, ram_mb=256, vm_version=8, operating_system_type=os, 
        thin_provision=True, disk_size_gb=100,  mac_address=None,
        network_name='VM Network',datastore_name=self.datastore_name )
        vm.power_on()

    def delopy_ova(self):
        obj=ova.deploymentOVF(host=self.host,user=self.user,port=self.port,password=self.password,
        disable_ssl_verification=True, ovf_path=self.path_,
        datacenter_name=None,resource_pool=None,datastore_name=None)
        obj.startDeploy()

    def power_off_(self,name):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    vm.power_off()
                    break

    def power_on_(self,vmname):
        client= self.obj
        name = vmname
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    vm.power_on()
                    break                

    def power_reboot_(self,name):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    vm.reboot()
                    break                 

    def _take_snap_(self,name,nameofsnap):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    vm.take_snapshot(nameofsnap, description="", memory=False, try_persist_disk=True)
                    break                
    def _get_snap_(self,name):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    a = vm.get_snapshots()
                    break
        return [i.name for i in a]

    def _delete_(self,name):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    vm.delete()
                    break  

    def _rename_(self,name,newname):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    vm.rename(newname)
                    break

    def _status_(self,name):
        client= self.obj
        for vm in client.get_virtual_machines():
                if vm.name == name:
                    a = vm.get_tools_status()
                    break
        return [i for i in a]


