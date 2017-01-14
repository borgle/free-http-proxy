#!/usr/bin/env python
# coding:utf-8

import logging
import mysql.connector
import mysql.connector.errors

from setting import Config
from singleton import Singleton


class MysqlStorager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._conn = mysql.connector.connect(**Config.MysqlServer)
        self._cursor = self._conn.cursor()

    def __del__(self):
        self._cursor.close()
        self._conn.close()

    def fetchone(self, sql, parameters=None):
        self._conn.ping(True, 3, 1)
        self._cursor.execute(sql, parameters)
        return self._cursor.fetchone()

    def fetchall(self, sql, parameters=None):
        self._conn.ping(True, 3, 1)
        self._cursor.execute(sql, parameters)
        return self._cursor.fetchall()

    def execute(self, sql, parameters=None, multi=False):
        self._conn.ping(True, 3, 1)
        self._cursor.execute(sql, parameters, multi)
        self._conn.commit()
        return self._cursor.rowcount