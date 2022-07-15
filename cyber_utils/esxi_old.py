#! /usr/bin/python3                                                                                                                    

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import atexit
import sys
import socket

MAX_DEPTH = 10
ssh_port = 22


def connect(host,user,pwd, domain_name='localhost.localdomain'):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    connection = SmartConnect(host=host, user=user, pwd=pwd, port=443, sslContext=context)
    atexit.register(Disconnect, connection)
    content = connection.RetrieveContent()
    return content

def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    container.Destroy()
    return obj

def enable_ssh(host,user,pwd, domain_name='localhost.localdomain'):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, ssh_port)
    result_of_check = a_socket.connect_ex(location)
    if result_of_check == 0:
        print("SSH already enabled")
    else:
        esxi_connection = connect(host,user,pwd, domain_name)
        host_system = get_obj(esxi_connection, [vim.HostSystem],domain_name)
        service_system = host_system.configManager.serviceSystem
        ssh_service = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
        service_system.Start(ssh_service.key)
        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            print("SSH enabled")
        else:
            print('Something goes wrong, SSH not enabled')
    a_socket.close()

def disable_ssh(host,user,pwd, domain_name='localhost.localdomain'):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, ssh_port)
    result_of_check = a_socket.connect_ex(location)
    if result_of_check != 0:
        print("SSH already closed")
    else:
        esxi_connection = connect(host,user,pwd, domain_name)
        host_system = get_obj(esxi_connection, [vim.HostSystem],domain_name)
        service_system = host_system.configManager.serviceSystem
        ssh_service = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
        service_system.Stop(ssh_service.key)
        result_of_check = a_socket.connect_ex(location)
        if result_of_check != 0:
            print("SSH disabled")
        else:
            print('Something goes wrong, SSH enabled yet')
    a_socket.close()

def print_vminfo(vm, depth=1):
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            print_vminfo(child, depth+1)
        return

    ip = vm.summary.guest.ipAddress
    if(ip == None): ip='Unreacheable'
    name = vm.summary.config.name
    print(str(name)+' '+str(ip))

def vms_info_name_ip(host,user,pwd):

    si = connect(host,user,pwd)
    for child in si.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                print_vminfo(vm)

#disable_ssh('192.168.174.131','root','R00t@123')
#vms_info_name_ip('192.168.174.131','root','R00t@123')

# check ssh open
##do some stuff for fun and profit
# close ssh 
#service_system.Stop(ssh_service.key) # Stop SSH service.