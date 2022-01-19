#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 Ryan Snodgrass

from .base import *
from ..util import *

import httpx
import pprint as pp


class RAKControl(HotspotControl):
    def __init__(self, ip):
        self._ip = ip

    def discover(ip):
        if is_port_open(ip, 8080):
            return 'rak'
        return None
