# APIC / SDK Version 2.3(1e)
# ACI Cobra SDK Modules
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
import cobra.model.fv as fvModels

#Disable Cert Warnings for Test Environment
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Import GetPass for password input masking
import getpass

#Prompt for user credentials
TacacsUser = raw_input('TACACS+ Username: ')
TacacsPassword = getpass.getpass()

# APIC Login Credentials
apicUrl = 'https://ssacimn010a02apic01.ss.astontech.com'
apicUsername = 'apic:TACACS\\' + TacacsUser
apicPassword = TacacsPassword
loginSession = LoginSession(apicUrl, apicUsername, apicPassword)

# Create a session with the APIC and login
moDir = MoDirectory(loginSession)
moDir.login()

# Start at the Top of MIT tree 
uniMo = moDir.lookupByDn('uni')

# Create a new Tenant MO and connect it as a Child object to the root of the MIM
# Call the new Tenant MO 'ExampleSdkTenant'
fvTenantMo = fvModels.Tenant(uniMo, 'ExampleSdkTenant')

# Create new Private network/VRF under the new Tenant
fvContextMo = fvModels.Ctx(fvTenantMo, 'myVRF')

#Create new BD under new Tenant
#fvBDMo = 

# Create a new configuration request to the APIC and pass in the new Tenant MO (including its children MOs)
# Commit the changes to the APIC
cfgRequest = ConfigRequest()
cfgRequest.addMo(fvTenantMo)
moDir.commit(cfgRequest)

# Log Out once the request is complete
moDir.logout()