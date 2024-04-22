import os
import socket
from argparse import ArgumentParser
import sys
import re
import json
import urllib.request


def trace(dist_ip):
    icmp_packet = b'\x08\x00\xf7\x4a\x00\x01\x00\xb4'
    connetion = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    ttl = 1
    cur_ip = None
    connetion.settimeout(5)
    while ttl != 30 and cur_ip != dist_ip:
        connetion.setsockopt(socket.SOL_IP, socket.IP_TTL, int(ttl))
        connetion.sendto(icmp_packet, (dist_ip, 33434))
        try:
            packet, ipPort = connetion.recvfrom(1024)
            cur_ip = ipPort[0]
            message = '%d)   %s' % (ttl, cur_ip)
            if public_ip(cur_ip):
                message += ' ' + str(simple_whois(cur_ip))
                yield message

            else:
                yield message + " its not public ip"
        except socket.timeout:
            yield '*****   TimeOUT   *****'
        ttl += 1
    connetion.close()


def public_ip(ip):
    local_ip_addresses_diapasons = (
        ('10.0.0.0', '10.255.255.255'),
        ('127.0.0.0', '127.255.255.255'),
        ('172.16.0.0', '172.31.255.255'),
        ('192.168.0.0', '192.168.255.255'))

    for diapason in local_ip_addresses_diapasons:
        if diapason[0] <= ip <= diapason[1]:
            return False
    return True


def init_parser():
    parser = ArgumentParser(prog="trace.py")
    parser.add_argument("-ip", action="store", help="ip to check.")
    return parser

def simple_whois(addr):
    data = json.loads(
        urllib.request.urlopen(
            'https://stat.ripe.net/data/prefix-overview/data.json?max_related=50&resource=%s' % addr).read())
    if len(data['data']['asns']) == 0:
        return '', '', ''
    as_name = data['data']['asns'][0]['asn']
    provider = data['data']['asns'][0]['holder']
    data = json.loads(
        urllib.request.urlopen('https://stat.ripe.net/data/rir/data.json?resource=%s&lod=2' %
                               addr).read())
    country = data['data']['rirs'][0]['country']
    return as_name, country, provider


if __name__ == '__main__':
    parse = init_parser()
    args = parse.parse_args()
    if args.ip is not None:
        for message in trace(args.ip):
            print(message)
