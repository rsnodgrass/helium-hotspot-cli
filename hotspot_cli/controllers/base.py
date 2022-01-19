#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 Ryan Snodgrass

class HotspotControl:
    def __init__(self):
        return

    def _methods(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_")]

    def info():
        return {}
