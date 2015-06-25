#!/usr/bin/python
# -*-coding:utf-8 -*

import subprocess
import sys

def get_fact(name, info="showvminfo"):
    mycleanfact={}
    try:
        cmd = "vboxmanage %s %s --machinereadable" % (info,name)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        fact = ps.communicate()
    except:
        return mycleanfact
    
    
    for i in fact[0].split("\n"):
        if "=" in i:
            valeur=i.split('=')[0]
            cle=i.split('=')[1]
            if valeur[0]=='"' and valeur[-1] == '"':
                valeur=valeur[1:-1]
            if cle[0]=='"' and cle[-1] == '"':
                cle=cle[1:-1]
            mycleanfact[valeur]=cle
    return mycleanfact

#print get_fact("disque", info="showhdinfo")
#print get_fact("lilo")


def createvm(module):
    # TODO : replace call by ckeck_output and search un std with regex
    rep=subprocess.call(["vboxmanage","createvm","--name",str(module.params['namevm']),"--ostype",str(module.params['types']),str(module.params['register'])])
    if rep == 0:
        module.exit_json(changed= True)
    elif rep == 1:
        module.exit_json(changed= False)
    else:
        print(rep)
#        module.fail_json(msg=" %s " % str(rep))
        module.fail_json(msg="problème avec la création de la vm ! ")

def suprvm(module):
    rep=subprocess.call(["vboxmanage",str(module.params['unregister']),str(module.params['namevm']),"-d"])
    if rep == 0:
        module.exit_json(changed= True)
    else:
        print(rep)
        module.fail_json(msg="problème avec la suppréssion de la vm ! ")


def createhd(module):
    rep=subprocess.call(["vboxmanage","showhdinfo",str(module.params['namehdd'])])
    if rep == 0:
        module.exit_json(changed= False)
    elif rep == 1:
        subprocess.call(["vboxmanage","createhd","--filename",str(module.params['namehdd']),"--size",str(module.params['taillehdd'])])
        module.exit_json(changed= True)
    else:
        module.fail_json(msg="problème avec la création de disque ! ")


#def test_sata(name, chemin, vm):
#    cmd = "vboxmanage showvminfo %s --machinereadable | grep %s-0-0 | cut -d '=' -f2" % (vm,name)
#    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#    fact = ps.communicate()[0][:-1]
#    print(fact)
#    return( fact == chemin)

def attach_storage(module, facts):
    if facts['sata-0-0'] != str(module.params['cheminstorage']):
        subprocess.call(["vboxmanage","storageattach",str(module.params['namevm']),"--storagectl",str(module.params['namestorage']),"--port",str(module.params['portstorage']),"--device",str(module.params['devicestorage']),"--type",str(module.params['typestorage']),"--medium",str(module.params['cheminstorage'])])
        module.exit_json(changed= True)
    else:
        module.exit_json(changed= False)

#def attach_storage(module):
#    if not test_sata("\"sata\"",str(module.params['cheminstorage']),str(module.params['namevm'])):
#        subprocess.call(["vboxmanage","storageattach",str(module.params['namevm']),"--storagectl",str(module.params['namestorage']),"--port",str(module.params['portstorage']),"--device",str(module.params['devicestorage']),"--type",str(module.params['typestorage']),"--medium",str(module.params['cheminstorage'])])
#        module.exit_json(changed= True)
#    else:
#        module.exit_json(changed= False)

def ajout_storage(module):
    rep2=subprocess.call(["vboxmanage","storagectl",str(module.params['namevm']),"--name",str(module.params['namestorage']),"--add",str(module.params['addstorage']),"--controller",str(module.params['controllerstorage'])])
    if rep2 == 0:
        module.exit_json(changed= True)
    elif rep2 == 1:
        module.exit_json(changed= False)
    else:
        print(rep)
        module.fail_json(msg= "problème avec le controleur de stockage ! ") 


#def test_valeur(name, valeur, vm):
#    cmd = "vboxmanage showvminfo %s --machinereadable | grep ^%s | cut -d '=' -f2" % (vm,name)
#    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#    fact = ps.communicate()[0][:-1]
#    print(fact)
#    return( fact == valeur)

#def modifyvm(module,facts):
#    if facts['memory'] != str(module.params['memory']):
#        if facts['vram'] != str(module.params['vram']):    
#            subprocess.call(["vboxmanage","modifyvm",str(module.params['namevm']),"--vram",str(module.params['vram'])])
#            module.exit_json(changed= True)
#        subprocess.call(["vboxmanage","modifyvm",str(module.params['namevm']),"--memory",str(module.params['memory'])])
#        module.exit_json(changed= True)
#    else:
#        module.exit_json(changed= False)

def modifyvm(module,facts):
    if facts['memory'] != str(module.params['memory']):
        subprocess.call(["vboxmanage","modifyvm",str(module.params['namevm']),"--memory",str(module.params['memory'])])
        module.exit_json(changed= True)
    else:
        module.exit_json(changed= False)




#def modifyvm(module):
#    if not test_valeur("memory", str(module.params["memory"]),str( module.params["namevm"])):
#        subprocess.call(["vboxmanage","modifyvm",str(module.params['namevm']),"--memory",str(module.params['memory'])])
#        module.exit_json(changed= True)
#    else:
#        module.exit_json(changed= False)



def main():
    module = AnsibleModule(
        argument_spec = dict(
            state = dict(default=None, choices=['present','absent','chois','present_hdd','controleur_stock','b_storage']),
            types = dict(default=None, choices=["Other_64","Windows31","Windows95","Windows98","WindowsMe","WindowsNT4","Windows2000","WindowsXP","WindowsXP_64","Windows2003","Windows2003_64","WindowsVista","WindowsVista_64","Windows2008","Windows2008_64","Windows7","Windows7_64","Windows8","Windows8_64","Windows81","Windows81_64","Windows2012_64","Windows10","Windows10_64","WindowsNT","WindowsNT_64","Linux22","Linux24","Linux24_64","Linux26","Linux26_64","ArchLinux","ArchLinux_64","Debian","Debian_64","OpenSUSE","OpenSUSE_64","Fedora","Fedora_64","Gentoo","Gentoo_64","Mandriva","Mandriva_64","RedHat","RedHat_64","Turbolinux","Turbolinux_64","Ubuntu","Ubuntu_64","Ubuntu_64","Xandros_64","Oracle","Oracle_64","Linux","Linux_64","Solaris","Solaris_64","OpenSolaris","OpenSolaris_64","Solaris11_64","FreeBSD","FreeBSD_64","OpenBSD","OpenBSD_64","NetBSD","NetBSD_64","OS2Warp3","OS2Warp4","OS2Warp45","OS2eCS","OS2","MacOS","MacOS_64","MacOS106","MacOS106_64","MacOS107_64","MacOS108_64","MacOS109_64","DOS","Netware","L4","QNX","JRockitVE"]),
            namevm = dict(default=None),
            register = dict(default='--register'),
            unregister = dict(default='unregistervm'),
            memory = dict(default=None),
            vram = dict(default=None),
            acpi = dict(default=None, choise=['off','on']),
            ioapic = dict(default=None, choise=['off','on']),
            cpu = dict(default=None),
            boot = dict(default=None, choise=['floppy','dvd','disk','net']),
            nic = dict(default=None, choise=['null','nat','bridged','intnet','host only']),
            bridgeadapter = dict(default=None),
            hostonlyadapter = dict(default=None),
            macaddress = dict(default=None, choise=['auto']),
            audio = dict(default=None, choise=['null','oss','pulse']),
            usb = dict(default=None, choise=['off','on']),
            usbehci = dict(default=None, choise=['off','on']),
            vrde = dict(default=None, choise=['off','on']),
            vrdeport = dict(default=None, choise=['default']),
            namehdd = dict(default=None),
            taillehdd = dict(default=None),
            namestorage = dict(default=None),
            addstorage = dict(default=None, choise=['ide','sata','scsi','floppy']),
            controllerstorage = dict(default='IntelAhci', choise=['LsiLogic','LSILogicSAS','BusLogic','PIIX3','PIIX4','ICH6','I82078']),
            portstorage = dict(default=None),
            devicestorage = dict(default=None),
            typestorage = dict(default=None, choise=['dvddrive','hdd','fdd']),
            cheminstorage = dict(default=None),

        ),
        supports_check_mode = True
    )
    facts=get_fact(str(module.params['namevm']))
    if module.params['state'] == 'present':
        createvm(module)
    if module.params['state'] == 'absent':
        if facts:
            suprvm(module)
        else:
            module.exit_json(changed= False)
    if module.params['state'] == 'chois':
        modifyvm(module,facts)
    if module.params['state'] == 'present_hdd':
        createhd(module)
    if module.params['state'] == 'controleur_stock':
        ajout_storage(module)
    if module.params['state'] == 'b_storage':
        attach_storage(module,facts)


#import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
