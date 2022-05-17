import imp
from .functions import *
from .tools import cli, service_instance
import atexit
from pyVim.connect import SmartConnect, Disconnect

class deploymentOVF:
    def connect(self):
        service_instance = None
        try:
            if self.disable_ssl_verification:
                service_instance = SmartConnect(host=self.host,
                                                user=self.user,
                                                pwd=self.password,
                                                port=self.port,
                                                disableSslCertValidation=True)
            else:
                print(">")
                service_instance = SmartConnect(host=self.host,
                                                user=self.user,
                                                pwd=self.password,
                                                port=self.port)

            atexit.register(Disconnect, service_instance)
        except IOError as io_error:
            print(io_error)

        if not service_instance:
            raise SystemExit("Unable to connect to host with supplied credentials.")

        return service_instance
    def __init__(self,host,ovf_path,user,port,password,disable_ssl_verification,datacenter_name,resource_pool,datastore_name):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.disable_ssl_verification = disable_ssl_verification
        self.ovf_path = ovf_path
        self.datacenter_name = datacenter_name
        self.resource_pool = resource_pool
        self.datastore_name = datastore_name
        
    def startDeploy(self):
        si = self.connect()

        if self.datacenter_name:
            datacenter = get_dc(si, args.datacenter_name)
        else:
            datacenter = si.content.rootFolder.childEntity[0]

        if self.resource_pool:
            resource_pool = get_rp(si, datacenter, self.resource_pool)
        else:
            resource_pool = get_largest_free_rp(si, datacenter)

        if self.datastore_name:
            datastore = get_ds(datacenter, self.datastore_name)
        else:
            datastore = get_largest_free_ds(datacenter)


        ovf_handle = OvfHandler(self.ovf_path)
        ovf_manager = si.content.ovfManager
        cisp = vim.OvfManager.CreateImportSpecParams()
        cisr = ovf_manager.CreateImportSpec(ovf_handle.get_descriptor(), resource_pool, datastore, cisp)

        if cisr.error:
            print("The following errors will prevent import of this OVA:")
            for error in cisr.error:
                print("%s" % error)
            return 1

        ovf_handle.set_spec(cisr)

        lease = resource_pool.ImportVApp(cisr.importSpec, datacenter.vmFolder)
        while lease.state == vim.HttpNfcLease.State.initializing:
            print("Waiting for lease to be ready...")
            time.sleep(1)

        if lease.state == vim.HttpNfcLease.State.error:
            print("Lease error: %s" % lease.error)
            return 1
        if lease.state == vim.HttpNfcLease.State.done:
            return 0

        print("Starting deploy...")
        return ovf_handle.upload_disks(lease, self.host)

