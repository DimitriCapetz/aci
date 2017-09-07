'''
This script will create all the pieces necessary to attach a host to a vpc pair.  All components are created from scratch
'''

#!/usr/bin/env python
# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fvns
import cobra.model.infra
import cobra.model.phys
import cobra.model.pol
from cobra.internal.codec.xmlcodec import toXMLStr

#Disable Cert Warnings for Test Environment
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Import GetPass for password input masking
import getpass

#Prompt for user credentials
apicIP = raw_input('APIC FQDN or IP: ')
TacacsUser = raw_input('TACACS+ Username: ')
TacacsPassword = getpass.getpass()

# APIC Login Credentials
apicUrl = 'https://' + apicIP
apicUsername = 'apic:TACACS\\' + TacacsUser
apicPassword = TacacsPassword
loginSession = cobra.mit.session.LoginSession(apicUrl, apicUsername, apicPassword)

# Create a session with the APIC and login
moDir = cobra.mit.access.MoDirectory(loginSession)
moDir.login()

# the top level object on which operations will be made
topMo = cobra.model.pol.Uni('')

# build the request using cobra syntax
serverList = ['ssesximn010a02aci03', 'ssacimn010a02aci04', 'ssacimn010a02aci05', 'ssacimn010a02aci06']
assignedPortofFirstServer = 11
port = assignedPortofFirstServer
for server_name in serverList:
    infraInfra = cobra.model.infra.Infra(topMo)
    infraFuncP = cobra.model.infra.FuncP(infraInfra)
    infraAccBndlGrp = cobra.model.infra.AccBndlGrp(infraFuncP, lagT='node', name=server_name + '_pol_grp')
    infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccBndlGrp, tDn='uni/infra/attentp-esx_aep')
    infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccBndlGrp, tnFabricHIfPolName='1Gb')
    infraRsLacpPol = cobra.model.infra.RsLacpPol(infraAccBndlGrp, tnLacpLagPolName='LACP_Active')
    infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccBndlGrp, tnCdpIfPolName='CDP_Disable')
    infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccBndlGrp, tnLldpIfPolName='LLDP_Enable')
    infraAccPortP = cobra.model.infra.AccPortP(infraInfra, 'leaf101-102_if_profile')
    infraHPortS = cobra.model.infra.HPortS(infraAccPortP, name=server_name + '_if_selector', type='range')
    infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name='block1', fromPort=str(port), toPort=str(port))
    infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, tDn='uni/infra/funcprof/accbundle-' + server_name + '_pol_grp')
    port = port + 1
    print toXMLStr(topMo)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    moDir.commit(c)


