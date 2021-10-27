import os
import time

import requests
from requests.auth import HTTPBasicAuth
import netifaces

ZONEEDIT_USERNAME = os.getenv('ZONEEDIT_USERNAME')
ZONEEDIT_TOKEN = os.getenv('ZONEEDIT_TOKEN')
ZONEEDIT_HOST_IPV6 = os.getenv('ZONEEDIT_HOST_IPV6')
ZONEEDIT_HOST_IPV4 = os.getenv('ZONEEDIT_HOST_IPV4')
IPV6_INTERFACE = os.getenv('IPV6_INTERFACE')


def obtain_ipv4():
    response = requests.get('http://checkip.dyndns.org/')
    # Current IP Address: 102.182.138.101
    return response.text.replace('<html><head><title>Current IP Check</title></head><body>Current IP Address: ', '').replace('</body></html>', '').strip()


def obtain_ipv6():
    addrs = netifaces.ifaddresses(IPV6_INTERFACE)
    return addrs[netifaces.AF_INET6][0]['addr']


def zoneedit_update(host, ip):
    # https://dynamic.zoneedit.com/auth/dynamic.html?host=$ddnshost&dnsto=$ipfresh
    response = requests.get(
        'https://dynamic.zoneedit.com/auth/dynamic.html',
        params={'host': host, 'dnsto': ip},
        auth = HTTPBasicAuth(ZONEEDIT_USERNAME, ZONEEDIT_TOKEN)
    )
    print("Response code:", response.status_code)
    print("Response text:", response.text)


if __name__ == '__main__':
    time.sleep(1)
    print("Starting")

    while True:
        ipv4 = obtain_ipv4()
        print("IPv4 setting", ZONEEDIT_HOST_IPV4, "to", ipv4)
        zoneedit_update(ZONEEDIT_HOST_IPV4, ipv4)

        print("Waiting 600 seconds")
        time.sleep(601)

        ipv6 = obtain_ipv6()
        print("IPv6 setting", ZONEEDIT_HOST_IPV6, "to", ipv6)
        zoneedit_update(ZONEEDIT_HOST_IPV6, ipv6)

        print("Waiting 600 seconds")
        time.sleep(601)
