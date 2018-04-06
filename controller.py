#!/usr/bin/env python
# coding:utf-8

from bottle import get, route, static_file
from bottle import request, jinja2_template

from setting import Config
from storager import MysqlStorager

db = MysqlStorager()


@get('/favicon.ico')
def favicon():
    return static_file("favicon.ico", root=Config.StaticRoot)


@get('/static/:filepath#(img|css|js|fonts)\/.+#')
def server_static(filepath):
    return static_file(filepath, root=Config.StaticRoot)


@route('/')
def home():
    rows = db.fetchall('select ip, port, lastcheck from http where failtimes<1 order by lastcheck desc limit 100')
    proxies = list()
    for row in rows:
        p = dict()
        p['ip'] = row[0]
        p['port'] = row[1]
        p['check'] = row[2]
        proxies.append(p)

    j = dict()
    j['proxies'] = proxies
    return jinja2_template('home.html', j)


@route('/chk.php')
def chk():
    # it was replaced by nginx
    x_real_ip = request.environ.get('HTTP_X_REAL_IP')
    via = request.environ.get('HTTP_VIA')
    x_forward_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    user_agent = request.environ.get('HTTP_USER_AGENT')
    accept_language = request.environ.get('HTTP_ACCEPT_LANGUAGE')

    result = {'remote_addr': x_real_ip, 'user_agent': user_agent, 'accept_language': accept_language}
    if via:
        result['via'] = via
    if x_forward_for:
        result['x_forward_for'] = x_forward_for

    ip = ','.join([x for x in (via, x_forward_for) if x])
    level = 'high anonymous'
    if ip:
        level = 'anonymous'
        if ip != x_real_ip:
            level = 'transparent'
    result['level'] = level

    return result
