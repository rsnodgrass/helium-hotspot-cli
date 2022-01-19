#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 Ryan Snodgrass

import os
import socket

from getmac import get_mac_address

LOCALHOST = '127.0.0.1'

HOSTS_BY_MAC = {}

def is_port_open(ip, port, timeout=0.1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def get_ip_prefix():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        prefix = st.getsockname()[0]
    except Exception:
        prefix = LOCALHOST
    finally:
        st.close()
    prefix = '.'.join(prefix.split('.')[:3])
    return prefix

def load_hosts_file(csv_file):
    try:
        input_csv = csv.DictReader(open(csv_file, 'r'), delimiter=';')
        for row in input_csv:
            hostname = row.get('hostname')
            if hostname:
                HOSTS_BY_MAC[row.get('mac').lower()] = hostname
    except:
        pass

def get_hostname(ip=None, mac=None):
    if mac:
        hostname = HOSTS_BY_MAC.get(mac.lower())
        if hostname:
            return hostname
    if ip:
        try:
            name, alias, addresslist = socket.gethostbyaddr(ip)
            return name
        except socket.error:
            pass
    return None
