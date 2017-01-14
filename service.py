#!/usr/bin/env python
# coding:utf-8
"""
  usage: %prog [options]
  fetch       :  run fetch module, this is default module.
  check       :  run check module
"""

__version__ = '1.0.0'

import logging, re, sys, random
import requests

from twisted.internet import reactor
from setting import Config
from storager import MysqlStorager


class Tasker(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Cache-Control': 'no-cache',
            }
        self.db = MysqlStorager()

    def _fetchHtml(self, pageurl):
        try:
            self.logger.debug(pageurl)
            self.headers['User-Agent'] = random.choice(Config.UserAgent)
            r = requests.get(pageurl, headers=self.headers, proxies=Config.Proxies)
            html = r.content
            return html
        except Exception as e:
            print e
            return ''

    def _saveproxies(self, proxies):
        # proxies = [x for x in proxies if x not in locals()['_[1]']]
        proxies = set(proxies)
        # print proxies
        '''过滤重复的数据，等同于“proxies = [elem for elem in proxies if porxies.count(elem) == 1]” '''
        for p in proxies:
            s = p.split(':')
            sqlparams = {'ip': s[0], 'port': int(s[1])}
            row = self.db.fetchone('select 1 from http where ip=%(ip)s, port=%(port)s', sqlparams)
            if row is None:
                sql = 'insert into http(ip, port) values(%(ip)s, %(port)s)'
                self.db.execute(sql, sqlparams)

    def freeproxylistsHttp(self):
        '''freeproxylists.com的http代理****************************代理非常的多****************************'''
        dic = [('anonymous.html', 'anon'), ('standard.html', 'standard')]
        dic.append(('us.html', 'us'))
        dic.append(('uk.html', 'uk'))
        dic.append(('ca.html', 'ca'))
        dic.append(('fr.html', 'fr'))
        # dic.append(('https.html', 'https'))
        dic.append(('elite.html', 'elite'))
        proxies = []
        pattern = re.compile('''&lt;td&gt;(\d+(\.\d+){3})&lt;/td&gt;&lt;td&gt;(\d+)&lt;/td&gt;''')
        for mm in dic:
            u = 'http://www.freeproxylists.com/%s' % mm[0]
            html = self._fetchHtml(u)
            us, matches = [], re.findall('''<a href='%s/d([^']+)\.html'>''' % mm[1],html)
            for g in matches:
                us.append(g)
            for uid in us:
                u = 'http://www.freeproxylists.com/load_%s_%s.html' % (mm[1],uid)
                html = self._fetchHtml(u)
                searchs = re.findall(pattern,html)
                for g in searchs:
                    proxies.append(g[0] + ':' + g[2])
                    self.logger.debug(g[0] + ':' + g[2])
        self._saveproxies(proxies)

    def freeproxylist(self):
        proxies = []
        pattern = re.compile('<tr><td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td><td>[^<]+</td><td>[^<]+</td><td>((elite proxy)|(anonymous))</td><td>[^<]+</td><td>[^<]+</td><td>[^<]+</td></tr>')
        u = 'http://free-proxy-list.net/'
        html = self._fetchHtml(u)
        #print html
        searchs = re.findall(pattern, html)
        for g in searchs:
            proxies.append(g[0] + ":" + g[1])
            self.logger.debug(g[0] + ':' + g[1])
        self._saveproxies(proxies)

    def fetch(self):
        self.freeproxylistsHttp()
        self.freeproxylist()
        reactor.callLater(60, self.fetch)

    def check(self):
        reactor.callLater(30, self.check)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    USAGE = __doc__.replace('%prog', sys.argv[0])
    if len(sys.argv) < 2:
        taskname = 'fetch'
    else:
        taskname = sys.argv[1]

    task = Tasker()
    func = getattr(task, taskname, None)
    if func is None:
        print USAGE
    else:
        reactor.callWhenRunning(func)
        reactor.run()