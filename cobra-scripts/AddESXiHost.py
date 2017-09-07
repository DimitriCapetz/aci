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
infraInfra = cobra.model.infra.Infra(topMo)
infraFuncP = cobra.model.infra.FuncP(infraInfra)
infraAccBndlGrp = cobra.model.infra.AccBndlGrp(infraFuncP, lagT=u'node', name=u'ssesximn010a02aci03_pol_grp')
infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccBndlGrp, tDn=u'uni/infra/attentp-esx_aep')
infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccBndlGrp, tnFabricHIfPolName=u'1Gb')
infraRsLacpPol = cobra.model.infra.RsLacpPol(infraAccBndlGrp, tnLacpLagPolName=u'LACP_Active')
infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccBndlGrp, tnCdpIfPolName=u'CDP_Disable')
infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccBndlGrp, tnLldpIfPolName=u'LLDP_Enable')
infraAccPortP = cobra.model.infra.AccPortP(infraInfra, 'leaf101-102_if_profile')
infraHPortS = cobra.model.infra.HPortS(infraAccPortP, name=u'ssesximn010a02aci03_if_selector', type='range')
infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block1', fromPort=u'12', toPort=u'12')
infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, tDn=u'uni/infra/funcprof/accbundle-ssesximn010a02aci03_pol_grp')


# commit the generated code to APIC
print toXMLStr(topMo)
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
moDir.commit(c)

