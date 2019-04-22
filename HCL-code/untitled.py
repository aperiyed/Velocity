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
dns_server = "172.17.153.121"

#checking nicIndex of first Nic

if os.environ['nicIndex'] == '1':
    networkId = os.environ['networkId']
    if networkId == 'Storage Controller Management Network':
        fvalue = '172.17.152.203'
        lvalue = '172.17.152.251'
        gwValue= '172.17.152.1'
        #gwValue = '.'.join(networkId.split("_")[-4:])  # This gives the network gateway value.
        networkDataValue = IPAddress(gwValue) - 1  # The network id required for Infoblox WAPI API.
        print "networkDataValue=" + networkDataValue
        nwValue = requests.get("https://172.17.152.121/wapi/v2.9/network", auth=('admin', 'infoblox'), verify=False,
                           data={'ipv4addr': networkDataValue, '_return_fields': 'network'})
        networkData = str(nwValue.json()[0]['network'])
        print "networkData=" + networkData
        ip = IPNetwork(networkData)
        network = str(ip.network)
        netmask = str(ip.netmask)
        gateway = str(gwValue)

# Setup connection object for Infoblox
iba_api = infoblox.Infoblox('172.17.152.121', 'admin', 'infoblox', '2.9',
                            iba_dns_view='default', iba_network_view='default', iba_verify_ssl=False)

try:
    # Create new host record with supplied network and fqdn arguments
    ip = iba_api.create_host_record(networkData, fvalue, lvalue, fqdn)
    print "DnsServerList=" + dns_server
    print "nicCount=1"
    print "nicIP_0=" + ip
    print "nicDnsServerList_0=" + dns_server
    print "nicGateway_0=" + gateway
    print "nicNetmask_0=" + netmask
    print "domainName=" + domain
    print "HWClockUTC=true"
    print "timeZone=Canada/Eastern"
    print "osHostname=" + hostname
    print "infobloxFQDN=" + fqdn
except Exception as e:
    print e



# Changes done to handle scenarios where existing BD is used when provisioning.

if os.environ['nicIndex'] == '2':
    if os.environ.get('ACIBDSubnetGW_1'):
        networkData = os.environ['ACIBDSubnetGW_1']
        ip = IPNetwork(networkData)
        network = str(ip.network)
        netmask = str(ip.netmask)
        gateway = str(ip.ip)
    else:
        networkId = os.environ['networkId']
        gwValue = '.'.join(networkId.split("_")[-4:])  # This gives the network gateway value.
        networkDataValue = IPAddress(gwValue) - 1  # The network id required for Infoblox WAPI API.
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
    ip = iba_api.create_host_record(networkData, fvalue, lvalue, fqdn)
    print "DnsServerList=" + dns_server
    print "nicCount=2"
    print "nicIP_1=" + ip
    print "nicDnsServerList_1=" + dns_server
    print "nicGateway_1=" + gateway
    print "nicNetmask_1=" + netmask
    print "domainName=" + domain
    print "HWClockUTC=true"
    print "timeZone=Canada/Eastern"
    print "osHostname=" + hostname
    print "infobloxFQDN=" + fqdn
except Except