######
Packer
######

#Dipendenze : https://github.com/josenk/terraform-provider-esxi

Si occupa del deployment, Crea dei .box dalle configurazioni .json le carica su ESXi
(tempo medio di deploy con iso: 20 minuti)
(tempo medio di deploy senza iso: 40 minuti)

#########
Terraform
#########

#Dipendenze : https://github.com/josenk/terraform-provider-esxi

Si occupa del provisioning, permette di clonare e/o modificare lo stato di macchine gia esistenti.


#######
Ansible
#######

//TO-DO
Si occupa di orchestrare la piattaforma.



#####
Vault
#####

Consente di passare a Terraform e Packer le credenziali tramite API HTTP da un server sicuro

###########
Cyber_utils
###########

Modulo/CLI Tool Python che permette di interagire con ESXi. Al momento supporta le seguenti operazioni:

-esxi.py (Dipendeze: https://github.com/vmware/pyvmomi)
    - Abilitare/disabilitare SSH senza accedere alla console web
    - Accendere/Spegnere tutte le macchine
    - Stampare informazioni riguardanti le macchine presenti (Nome,IP).

-packer.py
    -Mini Python Packer wrapper 

//TO-DO
-terraform.py
    -utility per clonare, modificare o distruggere macchine esistenti