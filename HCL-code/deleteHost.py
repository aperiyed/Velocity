#!/usr/bin/python
import infoblox, sys, requests, os, random
requests.packages.urllib3.disable_warnings()

#Assign command line arguments to named variables
infobloxFQDN = os.environ['infobloxFQDN']
iba_host = '172.17.152.121'
iba_wapi_version = 'v2.9'
base_url = 'https://' + iba_host + '/wapi/' + iba_wapi_version + '/'

domain = "noicldhcl.com"
if domain in infobloxFQDN:
    fqdn = infobloxFQDN
else:
    fqdn = infobloxFQDN + "." + domain

#Setup connection object for Infoblox
#Version 1.7 in call below correlated with version 6.12 of Infoblox
iba_api = infoblox.Infoblox('172.17.152.121', 'admin', 'infoblox', '2.9', 'default', 'default', False)

if os.environ.get("nicIndex") == '1':
    nicIP_0= os.environ.get("nicIP_0")
    nwRef = requests.get("https://172.17.152.121/wapi/v2.9/ipv4address", auth=('admin', 'infoblox'), verify=False,
                               data={'ip_address': nicIP_0})
    hostRef = str(nwRef.json()[0]['_ref'])

    rest_url = base_url + hostRef
    deleteReq = requests.delete(url=rest_url, auth=('admin','infoblox'), verify=False)

if os.environ.get("nicIndex") == '2':

    nicIP_0= os.environ.get("nicIP_0")
    print nicIP_0
    nwRef = requests.get("https://172.17.152.121/wapi/v2.9/ipv4address", auth=('admin', 'infoblox'), verify=False,
                               data={'ip_address': nicIP_0})
    print nwRef
    hostRef = str(nwRef.json()[0]['_ref'])
    print hostRef
    rest_url = base_url + hostRef
    deleteReq = requests.delete(url=rest_url, auth=('admin','infoblox'), verify=False)