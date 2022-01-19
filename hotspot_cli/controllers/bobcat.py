#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 Ryan Snodgrass
#
# Interesting, miners pool snapshot details from:
#  https://us915.s3.amazonaws.com/assets/snaps/snapshot.json

from .base import *

import httpx
import pprint as pp

BOBCAT_USER = 'bobcat'
BOBCAT_PASSWORD = 'miner'

TYPE_BOBCAT = 'bobcat'

class BobcatControl(HotspotControl):
    def __init__(self, ip):
        self._http = httpx.Client(base_url=f"http://{ip}", auth=(BOBCAT_USER, BOBCAT_PASSWORD), timeout=30)

    def discover(ip):
        try:
            response = httpx.get(f"http://{ip}/status.json")
            if response:
                j = response.json()
                if j.get('blockchain_height'):
                    return TYPE_BOBCAT
        except:
            pass
        return None

    def reboot(self):
        self._http.post("/admin/reboot")

    def reset(self):
        self._http.post("/admin/reset")
    
    def resync(self):
        self._http.post("/admin/resync")

    def fastsync(self):
        self._http.post("/admin/fastsync")

    def status(self):
        response = self._http.get("/status.json")
        pp.pprint(response.json())

    def peers(self):
        response = self._http.get("/peerbook.json")
        pp.pprint(response.json())

    def name(self):
        response = self._http.get("/miner.json")
        name = response.json().get('animal')
        print(name)
        return name

    def info(self):
        response = self._http.get("/miner.json")
        pp.pprint(response.json())
