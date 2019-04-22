#!/usr/bin/python
import infoblox, sys, requests, os, random
from netaddr import *

requests.packages.urllib3.disable_warnings()

# Assign command line arguments to named variables
# and declare variables with default values.
hostname = os.environ['vmName']
networkData = ''
netmask = ''
gateway = ''
ip = ''
domain = "noicldhcl.com"
fqdn = hostname + "." + domain
dns_server = "172.17.152.121"
fvalue = ""
lvalue = ""
broadcast = ""
dnsConfig = ""


# Changes done to handle scenarios where existing BD is used when provisioning.
if os.environ.get("nicIndex") == '1':
    networkData = "172.17.152.0/24"
    network = "172.17.152.0"
    netmask = "255.255.255.0"
    gateway = "172.17.152.254"
    fvalue = "172.17.152.203"
    lvalue = "172.17.152.253"
    dnsConfig = "false"
else:
    dnsConfig = "true"
    if os.environ.get('ACIBDSubnetGW_2'):
        networkData = os.environ['ACIBDSubnetGW_2']
        ip = IPNetwork(networkData)
        network = str(ip.network)
        netmask = str(ip.netmask)
        gateway = str(ip.ip)
        broadcast = str(ip.broadcast)
        ip_range = [ip for ip in IPNetwork(networkData) if
                    ip not in [IPAddress(gateway), IPAddress(network), IPAddress(broadcast)]]
        fvalue = str(ip_range[0])
        lvalue = str(ip_range[len(ip_range) - 1])
    else:
        networkId = os.environ['networkId']
        print networkId
        gwValue = '.'.join(networkId.split("_")[-4:])  # This gives the network gateway value.
        print gwValue
        networkDataValue = IPAddress(gwValue) - 1  # The network id required for Infoblox WAPI API.
        print networkDataValue
        nwValue = requests.get("https://172.17.152.121/wapi/v2.9/network", auth=('admin', 'infoblox'), verify=False,
                               data={'ipv4addr': networkDataValue, '_return_fields': 'network'})
        networkData = str(nwValue.json()[0]['network'])
        ip = IPNetwork(networkData)
        network = str(ip.network)
        netmask = str(ip.netmask)
        gateway = str(gwValue)
        broadcast = str(ip.broadcast)
        ip_range = [ip for ip in IPNetwork(networkData) if
                    ip not in [IPAddress(gateway), IPAddress(network), IPAddress(broadcast)]]
        fvalue = str(ip_range[0])
        lvalue = str(ip_range[len(ip_range) - 1])
# Setup connection object for Infoblox
iba_api = infoblox.Infoblox('172.17.152.121', 'admin', 'infoblox', '2.9',
                            iba_dns_view='default', iba_network_view='default', iba_verify_ssl=False)

try:
    # Create new host record with supplied network and fqdn arguments
    ip = iba_api.create_host_record(networkData, fvalue, lvalue, fqdn, dnsConfig)
    print "DnsServerList=" + dns_server
    print "nicCount=1"
    print "nicIP_0=" + ip
    print "nicDnsServerList_0=" + dns_server
#    if os.environ.get("nicIndex") != '1':
    print "nicGateway_0=" + gateway
    print "nicNetmask_0=" + netmask
    print "domainName=" + domain
    print "HWClockUTC=true"
    print "timeZone=Canada/Eastern"
    if os.environ['eNV_osName'] == "Windows":
        custSpec=Win2k16CustSpec
        hwClockUTC = "true"
        timeZoneId = '190'
	fullName = "HCL"
  	organization = "HCL"
	productKey = "MPJ7N-TK7YH-74WYQ-687YC-9QCG4"
	setAdminPassword = "HCLcl0ud"
	dynamicPropertyName = "cliqr"
        changeSid = "true"
        deleteAccounts = "false"
	    print "timeZoneId=" + timeZoneId                # Pacific Standard Tim
        print "fullName=" + fullName
        print "organization=" + organization
        print "productKey=" + productKey
        print "changeSid=" + changeSid
        print "setAdminPassword=" + setAdminPassword
        print "deleteAccounts=" + deleteAccounts
        print "dynamicPropertyName=" + dynamicPropertyName

    print "osHostname=" + hostname
    print "infobloxFQDN=" + fqdn
except Exception as e:
    print e