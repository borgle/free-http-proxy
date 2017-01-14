#!/usr/bin/env python
# coding:utf-8
import os


class Config(object):
    WebRoot = os.path.dirname(os.path.abspath(__file__))
    StaticRoot = os.path.join(WebRoot, 'static')

    Proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}

    MysqlServer = {
            'user': 'proxy',
            'password': 'proxy.Mysql.8',
            'host': '127.0.0.1',
            'database': 'proxy',
            'charset': 'utf8mb4',
            'raise_on_warnings': True,
        }

    MemcachedServer = ['127.0.0.1:11211']

    UserAgent = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
            'Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+6.0;+.NET+CLR+3.0.04506;)',
            'Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+Trident/4.0;+.NET+CLR+2.0.50727;+yie8)',
            'Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+.NET+CLR+2.0.50727;+GreenBrowser)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+icafe8)',
            'Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+Trident/4.0)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+MAXTHON+2.0)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+QQPinyinSetup+614)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+CIBA;+.NET+CLR+2.0.50727)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+CIBA;+.NET+CLR+3.0.4506.2152;+.NET+CLR+3.5.30729)',
            'Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+.NET+CLR+1.1.4322;+.NET+CLR+2.0.50727;+CIBA)',
            'Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+.NET+CLR+2.0.50727;+CIBA)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+CIBA;+.NET+CLR+1.1.4322;+MAXTHON+2.0)',
            'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.2;+Trident/4.0;+Mozilla/4.0+;+InfoPath.1)',
            'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+InfoPath.2;+MAXTHON+2.0)'
        ]

    SessionOptions = {
            'session.type': 'ext:memcached',
            'session.cookie_expires': 300,
            'session.url': MemcachedServer[0],
            'session.key': 'auth_token',
            'session.httponly': True,
            'session.auto': True
        }