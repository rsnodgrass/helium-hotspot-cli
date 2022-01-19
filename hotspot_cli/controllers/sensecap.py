#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 Ryan Snodgrass
#
# For API usage instructions goto: https://status-api-doc.sensecapmx.cloud/
# ToDo: Make it a serverless web based GUI using https://pywebview.flowrl.com/examples/
#
# https://status.sensecapmx.cloud/#/hotspot/list

from .base import *

import re
import httpx

TYPE_SENSECAP = 'sensecap'

class SenseCAPControl(HotspotControl):

    class SenseCAPAuth(httpx.Auth):
        def __init__(self, controller, ip, cpu_id, token=None):
            self._controller = controller
            self._ip = controller._ip
            self._cpu_id = controller._cpu_d
            self._token = token
            self._cookie = None

            # NOTE: SenseCAP web interface uses a session cookie
            self._http = httpx.Client(base_url=f"http://{ip}/login", timeout=30)

        # send the request with a custom `Authorization` header
        def auth_flow(self, request):
            if self._token:
                request.headers['Authorization'] = 'Basic ' + self._token
            return request

        # return an `httpx.Request` for refreshing tokens
        def build_refresh_request(self):
            return httpx.Request("POST", f"http://{ip}/login", data={ 'cpuid': self._cpu_id }) 

        # update the authorization token from a refresh request
        def update_tokens(self, response):
            self._cookies = response.cookies

            # extra the API token
            match = re.search('Your device token: (.*)</div>', response.content)
            if match:
                self._token = match.group(0)
                self._controller._token = self._token
                LOG.warning(f"CPU id {self._cpu_id}={self._token}")

    def __init__(self, ip, cpu_id):
        self._ip = ip
        self._cpu_id = cpu_id
        self._token = None
        self._http = httpx.Client(base_url=f"http://{ip}", auth=SenseCAPAuth(controller))

    def discover(ip):
        try:
            response = httpx.get(f"http://{ip}/login")
            if 'SenseCAP' in response.text:
                return TYPE_SENSECAP
        except:
            pass
        return False

    def reboot(self):
        self._http.post('/reboot')

    def shutdown(self):
        self._http.post('/shutdown')

    def resetblocks(self):
        self._http.post('/resetblocks')

    def turbosync(self):
        self._http.post('/turbosync')

    def info(self):
        info = {
            'ip': self._ip,
            'cpu_id': self._cpu_id,
            'token': self._token
        }
        return info
