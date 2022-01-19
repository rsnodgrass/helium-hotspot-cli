#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 Ryan Snodgrass
#
# For API usage instructions goto: https://status-api-doc.sensecapmx.cloud/
# ToDo: Make it a serverless web based GUI using https://pywebview.flowrl.com/examples/
#
# https://status.sensecapmx.cloud/#/hotspot/list

from .base import *

import pprint as pp

import time
import httpx

def convert_time(x):
    epoch = []
    for i in range(len(x)):
        result = time.ctime(x[i]/1000)
        epoch.append(result)
    return epoch

def convert_single_time(x):
    return time.ctime(x/1000)

def time_between(d, type):    
    time_table = list_data(d['syncList'], 'time')
    block_table = list_data(d['syncList'], type)
    time_between = ((time_table[0]-time_table[6])/1000)*2
    rate = (block_table[0] - block_table[6])*2
    return rate

def rate(list,type):
    y1 = list_data(list['syncList'], type)[11]
    y2 = list_data(list['syncList'], type)[0]
    x1 = 1
    x2 = 12
    return (y2-y1)/(x2-x1)
    

def list_data(block,k):
    return [sub[k] for sub in block]

def P2P_status(d):
    if d == 1:
        return "Healthy" 
    if d == 0:
        return "Unhealthy"
    else:
        return "Unknown"

def online_status(d):
    if d is True:
        return "Yes"
    if d is False:
        return "No"
    else:
        return "Unknown Error"

def relay_status(d):
    if d == 1:
        return "Yes"
    if d == 2:
        return "No"
    else:
        return "Unknown Error"

def fan_status(d):
    if d == 0:
        return "On"
    if d == 1:
        return "Off"
    else:
        return "Unknown Error"

class HotspotControl:
    def __init__(self):
        return

    def _methods(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_")]

# see https://status-api-doc.sensecapmx.cloud
class SenseCAPCloudControl(HotspotControl):

    def __init__(self, api_key, serial_number):
        self._serial = serial_number
        self._base_url = f"https://status.sensecapmx.cloud/api/openapi/device"
        self._url_args = f"?sn={serial_number}&api_key={api_key}"
        self._http = httpx.Client(base_url=self._base_url)

        self._data_list = ('collectTime', 'height', 'totalHeight', 'connected', 'dialable', 'name', 'synced', 'online', 'heliumOnline',
             'isHealth', 'relayed', 'syncList', 'cpuTemperature', 'fan_status_list', 'cpuUsed', 'memoryTotal',
             'memoryUsed', 'sdTotal', 'sdUsed')

    def discover(ip):
        return False


    def raw_info(self):
        response = self._http.get('/view_device' + self._url_args)
        pp.pprint(response.json())

    def info(self):
        response = self._http.get('/view_device' + self._url_args)
        j = response.json()

        data = {}
        for i in range(len(self._data_list)):
            data[self._data_list[i]] = recursive_lookup(self._data_list[i], j)
    
        net_blocks = time_between(data, 'height') - time_between(data, 'total')
        blocks_togo = data['totalHeight'] - data['height']
        hours_togo = blocks_togo / net_blocks

        print("\n      " + data['name'].upper() + " SYNC & DIAGNOSTICS TOOL" )
        print("\n                        SYNC RATE                                      ")
        print("-----------------------------------------------------------------------\n")
        print("Time of Last Block Synced:                    " + str(convert_single_time(data['collectTime'])))
        print("Approx. Height Added Per Hour:                " + str(time_between(data,'height')))
        print("Approx. Helium Height Added Per Hour:         " + str(time_between(data,'total')))
        print("Approx. Net Height Added Per Hour:            " + str(net_blocks))
        print("Approx. Hours To Sync:                        " + str(round(hours_togo,2)))
        print("Sync Percent:                                 " + str(round(data['height']/data['totalHeight'],4)*100) + "%")
        print("My Current Block Height:                      " + str(data['height']))
        print("Helium Block Height:                          " + str(data['totalHeight']))
        print("Blocks To Go:                                 " + str(data['totalHeight']-data['height']))
        print("\n                       NETWORK STATUS                                  ")
        print("-----------------------------------------------------------------------\n")
        print("Helium Online:                                " + online_status(data['heliumOnline']))
        print("Online:                                       " + online_status(data['online']))
        print("Synced:                                       " + online_status(data['synced']))
        print("Relayed:                                      " + relay_status(data['relayed']))
        print("P2P Outbound:                                 " + P2P_status(data['connected']))
        print("P2P Inbound:                                  " + P2P_status(data['dialable']))
        print("\n                       DEVICE DIAGNOSTICS                              ")
        print("-----------------------------------------------------------------------\n")
        print("SD Used:                                      " + str(round(data['sdUsed']/data['sdTotal'],4)*100) +"%")
        print("SD Free:                                      " + str(100-round(data['sdUsed']/data['sdTotal'],4)*100) +"%")
        print("Memory Used:                                  " + str(round(data['memoryUsed']/data['memoryTotal'],4)*100) +"%")
        print("Memory Free:                                  " + str(100-round(data['memoryUsed']/data['memoryTotal'],4)*100) +"%")
        print("CPU Temperature:                              " + str(data['cpuTemperature']) + " C")
        print("Fan Temp:                                     " + str(list_data(data['fan_status_list'], 'temperature')[0]) + " C")
        print("Fan Status:                                   " + fan_status(list_data(data['fan_status_list'], 'fan')[0]))
