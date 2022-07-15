import re
from hcl_vm import VM
from hcl_login import Login

def parse(filepath):
    _login = Login()
    init=True
    name=''
    args=list()
    collection=list()
    par_counter=0
    adding=False
    result=list()
    with open(filepath,"r") as lines:
        for line in lines: 
            if(init):
                if '}' in line:
                    init = False
                elif(re.match(".*=.*",line)):
                    if 'hostname' in line:
                        _login.hostname=re.split("=",line.replace(" ",""))[1]
                    elif 'hostport' in line:
                        _login.hostport=re.split("=",line.replace(" ",""))[1]
                    elif 'username' in line:
                        _login.username=re.split("=",line.replace(" ",""))[1]
                    elif 'password' in line:
                        _login.password=re.split("=",line.replace(" ",""))[1]
                elif(re.match("^provider",line.replace("\n",""))):
                    _login.provider = re.split(" ",line.replace("\n",""))[1]
            elif(re.match("^resource",line.replace("\n",""))) and par_counter == 0 and not adding :
                name=re.split(" ",line.replace("\n",""))[2]
                par_counter += 1
            elif(re.match("^[^{}#]*=[^{}#]*$",line))  and par_counter > 0 and not adding:
                param=re.split('=',line.replace(' ','').replace('\n',''))
                collection.append(param)
            elif '{' in line and not adding:
                adding = True
                par_counter+=1
                args=list()
                args.append(line.replace(' ',"").replace('{',"").replace("\n",""))
            elif(adding):
                if('}' in line):
                    adding=False
                    par_counter-=1
                    collection.append(args)
                else:
                    args.append(re.split("=",line.replace(" ","").replace("\n","")))
            elif('}' in line):
                par_counter -= 1
                vm = VM(name,params=collection)
                result.append(vm)
                name=''
                collection=list()
    return _login,result
                
# k = Login()
x,k = parse('/home/tosqui/lab/Terraform/main.tf')
print(x.provider.replace('"',''))
x.provider = 'cicciu'
print(k[0].params)
# for vm in x:
#     print("\n\n\n\n")
#     print(vm.params)
#     print("\n\n\n\n")
