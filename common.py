#!/usr/bin/env python
# coding:utf-8

import datetime

class UTC(datetime.tzinfo):
    """UTC"""
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return datetime.timedelta(hours=self._offset)