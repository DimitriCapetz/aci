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
physDomP = cobra.model.phys.DomP(topMo, name=u'test_arya_dom')
infraInfra = cobra.model.infra.Infra(topMo)
infraAttEntityP = cobra.model.infra.AttEntityP(infraInfra, name=u'test_arya_aep')
infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn=u'uni/phys-test_arya_dom')
infraFuncP = cobra.model.infra.FuncP(infraInfra)
infraAccBndlGrp = cobra.model.infra.AccBndlGrp(infraFuncP, lagT=u'node', name=u'test_arya_vpc_pol_grp')
infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccBndlGrp, tDn=u'uni/infra/attentp-test_arya_aep')
infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccBndlGrp, tnFabricHIfPolName=u'1Gb')
infraRsLacpPol = cobra.model.infra.RsLacpPol(infraAccBndlGrp, tnLacpLagPolName=u'LACP_Active')
infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccBndlGrp, tnCdpIfPolName=u'CDP_Enable')
infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccBndlGrp, tnLldpIfPolName=u'LLDP_Enable')
fvnsVlanInstP = cobra.model.fvns.VlanInstP(infraInfra, name=u'test_arya_vlan', allocMode='dynamic')
fvnsEncapBlk = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-299', from_=u'vlan-199', allocMode='inherit')
infraAccPortP = cobra.model.infra.AccPortP(infraInfra, name=u'leaf101-102-arya_if_profile')
infraHPortS = cobra.model.infra.HPortS(infraAccPortP, name=u'leaf101-102-arya_if_selector', type='range')
infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block1', fromPort=u'37', toPort=u'37')
infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, tDn=u'uni/infra/funcprof/accbundle-test_arya_vpc_pol_grp')
infraNodeP = cobra.model.infra.NodeP(infraInfra, name=u'leaf101-102-arya_profile')
infraLeafS = cobra.model.infra.LeafS(infraNodeP, type=u'range', name=u'leaf101-102-arya_sw_selector')
infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafS, to_=u'102', from_=u'101', name=u'e6387402a5b7303b')
infraRsAccPortP = cobra.model.infra.RsAccPortP(infraNodeP, tDn=u'uni/infra/accportprof-leaf101-102-arya_vpc_if_profile')


# commit the generated code to APIC
print toXMLStr(topMo)
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
moDir.commit(c)

