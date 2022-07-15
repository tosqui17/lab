#! /usr/bin/python3                                                                                                                    

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import requests.packages.urllib3 as urllib3
from hcl_vm import VM
import re
import ssl
import atexit
import sys
import socket
import json


MAX_DEPTH = 12
SSH_PORT = 22

host = ''
user = '' 
pwd = ''
domain = '' 


def set_user(_user):
    global user
    user = _user

def set_host(_host):
    global host
    host = _host

def set_pwd(_pwd):
    global pwd
    pwd = _pwd

def set_domain(_domain):
    global domain
    domain = _domain

def connect():
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

def enable_ssh():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, SSH_PORT)
    result_of_check = a_socket.connect_ex(location)
    if result_of_check == 0:
        print("SSH already enabled")
    else:
        esxi_connection = connect()
        host_system = get_obj(esxi_connection, [vim.HostSystem],domain)
        service_system = host_system.configManager.serviceSystem
        ssh_service = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
        service_system.Start(ssh_service.key)
        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            print("SSH enabled")
        else:
            print('Something goes wrong, SSH not enabled')
    a_socket.close()

def disable_ssh():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, SSH_PORT)
    result_of_check = a_socket.connect_ex(location)
    if result_of_check != 0:
        print("SSH already closed")
    else:
        esxi_connection = connect()
        host_system = get_obj(esxi_connection, [vim.HostSystem],domain)
        service_system = host_system.configManager.serviceSystem
        ssh_service = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
        service_system.Stop(ssh_service.key)
        result_of_check = a_socket.connect_ex(location)
        if result_of_check != 0:
            print("SSH disabled")
        else:
            print('Something goes wrong, SSH enabled yet')
    a_socket.close()

def vm_info(vm, depth=1):
    result = VM('',[])
    result.name=vm.summary.config.name
    #HCL compatible
    result.params.append(add_param('ovf_source',vm.summary.config.vmPathName))
    result.params.append(add_param('guest_name',vm.summary.config.name))
    result.params.append(add_param('boot_disk_type','thin'))
    result.params.append(add_param('disk_store',vm.summary.config.vmPathName))
    result.params.append(add_param('memsize',str(vm.summary.config.memorySizeMB)))
    result.params.append(add_param('numvcpus',str(vm.summary.config.numCpu)))
    result.params.append(add_param('ip',str(vm.summary.guest.ipAddress)))
    #doesn't work properly
    result.params.append(add_param('boot_disk_size',str((vm.summary.storage.committed//1000000000))))
    tmp='off'
    if('On' in vm.summary.config.name):
        tmp='on'
    result.params.append(add_param('power',tmp))
    for i in range(len(vm.config.hardware.device)):
        if(isinstance(vm.config.hardware.device[i],vim.vm.device.VirtualVmxnet) or isinstance(vm.config.hardware.device[i],vim.vm.device.VirtualEthernetCard)):
            to_add=list()
            to_add.append('virtual_network')
            to_add.append(vm.config.hardware.device[i].deviceInfo.summary)
            result.params.append(add_param('network_interfaces',to_add))
    return result

def add_param(key,value):
    if(isinstance(value,str)):
        tmp=key
        tmp+=','
        tmp+="\""
        #tricky
        tmp+= re.split(" ",value)[0][1:-1] if key == 'disk_store' else re.sub("\[.*\] ",'',value.strip())
        tmp+="\""
        return re.split(",",tmp)
    elif(isinstance(value,list)):
        tmp=list()
        tmp.append(key)
        tmp.append(value)
        return tmp
    
def vms_list():
    result = list() 
    instance = connect()
    for child in instance.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                result.append(vm_info(vm))
    return result

def power_on_all():
    instance=connect()
    obj_view = instance.viewManager.CreateContainerView(instance.rootFolder, [vim.VirtualMachine], True)
    vm_list = obj_view.view
    for vm in vm_list:
        vm.PowerOn()

def power_off_all():
    instance=connect()
    obj_view = instance.viewManager.CreateContainerView(instance.rootFolder, [vim.VirtualMachine], True)
    vm_list = obj_view.view
    for vm in vm_list:
        vm.PowerOff()
