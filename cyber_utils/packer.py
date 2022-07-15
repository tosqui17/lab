#! /usr/bin/python3                                                                                                                    
import subprocess
import platform

PACKER = ''

try:
    if platform.system == 'Windows':
        result = subprocess.run(["powershell","-e","Get-Command packer | Select Source -ExpandProperty Source"], text=True, stdout=subprocess.PIPE,check=true).returncode
        PACKER  = result.stdout
    else:
        result = subprocess.run(["which","packer"], text=True, stdout=subprocess.PIPE,check=True)
        PACKER = result.stdout[:-1]
except:
    print("Something goes wrong finding Packer Path")
    exit(-1)

def run(args):
    cmd= list()
    cmd.append(PACKER)
    cmd.append(args)
    try:
        result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as c:
        print(c.stdout)
        exit(-1)

def init(upgrade=False):
    if(upgrade): run('init -upgrade')
    run('init')

def validate(template, var_file=''):
    if(not var_file): run('validate '+template)
    else: run('validate -var-file '+var_file+' '+template)
    run('validate ' + template) if not var_file else run('validate -var-file ' + varfile + ' ' + template) 

def build(template, debug = False, var_file = ''):
    cmd = '-debug ' if not debug else ''
    cmd += '-var-file '+var_file+' ' if not var_file else ''
    cmd += template
    run(cmd)

build('x')
    
