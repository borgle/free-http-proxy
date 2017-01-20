#!/usr/bin/env python
# coding:utf-8
"""
  usage: %prog [options]
  fetch       :  run fetch module, this is default module.
  check       :  run check module
"""

__version__ = '1.0.0'

import logging, re, sys, random, urllib2, base64
import requests
import gevent
from gevent import monkey

from setting import Config
from storager import MysqlStorager


class Tasker(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = MysqlStorager()

    def _fetchHtml(self, pageurl, data=None, proxies = Config.Proxies, referer=None, timeout=None):
        try:
            self.logger.debug(pageurl)
            headers = {
                'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Cache-Control': 'no-cache',
            }
            headers['User-Agent'] = random.choice(Config.UserAgent)
            if referer:
                headers['Referer'] = referer
            if data:
                r = requests.post(pageurl, headers=headers, proxies=proxies, timeout=timeout)
            else:
                r = requests.get(pageurl, headers=headers, proxies=proxies, timeout=timeout)
            html = r.content
            return html
        except Exception as e:
            self.logger.error(e.message)
            return ''

    def _save_proxies(self, proxies):
        # proxies = [x for x in proxies if x not in locals()['_[1]']]
        proxies = set(proxies)
        # print proxies
        '''过滤重复的数据，等同于“proxies = [elem for elem in proxies if porxies.count(elem) == 1]” '''
        for p in proxies:
            s = p.split(':')
            sqlparams = {'ip': s[0], 'port': int(s[1])}
            row = self.db.fetchone('select 1 from http where ip=%(ip)s and port=%(port)s', sqlparams)
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
        pattern = re.compile('''&lt;td&gt;(\d+(\.\d+){3})&lt;/td&gt;&lt;td&gt;(\d+)&lt;/td&gt;''')
        for mm in dic:
            proxies = []
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
                gevent.sleep(0.3)
            self._save_proxies(proxies)

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
        self._save_proxies(proxies)

    def cnproxyHttp(self):
        '''获取cnproxy.com的http代理'''
        proxies = []
        pattern = re.compile(
            '<td>(\d+\.\d+\.\d+\.\d+)<SCRIPT type=text/javascript>document\.write\(":"((\+[a-z]){2,5})\)</SCRIPT></td><td>HTTP</td>')
        script = re.compile('''<SCRIPT type="text/javascript">\n(([a-z]="(\d)";)+)</SCRIPT>''')

        us = [['http://www.cnproxy.com/proxyedu%s.html', 4]]
        us.append(['http://www.cnproxy.com/proxy%s.html', 10])
        for u in us:
            for i in range(1, u[1] + 1):
                url = u[0] % i
                html = self._fetchHtml(url)
                scripts = re.search(script, html)
                if scripts:
                    t = scripts.group(1).strip(';').replace('"', '')
                    s = {}
                    for d in t.split(';'):
                        v = d.split('=')
                        s[v[0]] = v[1]
                    searchs = re.findall(pattern, html)
                    for g in searchs:
                        p = g[0] + ":"
                        for d in g[1].strip('+').split('+'):
                            p = p + s[d]
                        proxies.append(p)
                        self.logger.debug(p)
        self._save_proxies(proxies)

    def ipcnorgHttp(self):
        '''获取proxy.ipcn.org的http代理'''
        proxies = []
        pattern = re.compile('''(\d+(\.\d+){3}:\d{2,4})''')
        url = 'http://proxy.ipcn.org/proxylist2.html'
        html = self._fetchHtml(url)
        searchs = re.findall(pattern, html)
        for g in searchs:
            proxies.append(g[0])
            self.logger.debug(g[0])
        self._save_proxies(proxies)

    def samairruHttp(self):
        '''获取samair.ru的http代理'''
        proxies = []
        script = re.compile('''<script type="text/javascript">\n(([a-z]=(\d);)+)</script>''')
        pattern = re.compile(
            '<tr class="(elite|anon[^"]+)"><td>(\d+\.\d+\.\d+\.\d+).+?document\.write\(":"((\+[a-z]){2,5})\)</script></td>')
        for i in range(1, 5):
            u = 'http://www.samair.ru/proxy/proxy-%s.htm' % (('0' + str(i))[-2:])
            html = self._fetchHtml(u)
            scripts = re.search(script, html)
            if scripts:
                t = scripts.group(1).strip(';')
                s = {}
                for d in t.split(';'):
                    v = d.split('=')
                    s[v[0]] = v[1]
                searchs = re.findall(pattern, html)
                for g in searchs:
                    p = g[1] + ":"
                    for d in g[2].strip('+').split('+'):
                        p = p + s[d]
                    proxies.append(p)
                    self.logger.debug(p)
        self._save_proxies(proxies)

    def nntimeHttp(self):
        '''获取nntime.com的http代理'''
        proxies = []
        pattern = re.compile(
            '''<td>(\d+\.\d+\.\d+\.\d+).+?document\.write\(":"((\+[a-z]){2,5})\)</script></td>\n<td>(high\-anon|anon)[^<]*?</td>''')
        script = re.compile('''<script type="text/javascript">\n(([a-z]=(\d);)+)</script>''')
        for i in range(1, 30):
            u = 'http://nntime.com/proxy-list-%s.htm' % (('0' + str(i))[-2:])
            html = self._fetchHtml(u)
            scripts = re.search(script, html)
            if scripts:
                t = scripts.group(1).strip(';')
                s = {}
                for d in t.split(';'):
                    v = d.split('=')
                    s[v[0]] = v[1]
                searchs = re.findall(pattern, html)
                for g in searchs:
                    p = g[0] + ":"
                    for d in g[1].strip('+').split('+'):
                        p = p + s[d]
                    proxies.append(p)
                    self.logger.debug(p)
        self._save_proxies(proxies)

    def xroxyHttp(self):
        '''xroxy.com'''
        proxies = []
        pattern = re.compile('''<tr class='row[01]'>.*?</tr>''')
        a = re.compile('>(\d+\.\d+\.\d+\.\d+)')
        b = re.compile("'>(\d{2,5})</a>")
        uid = 0
        while True:
            u = 'http://www.xroxy.com/proxylist.php?type=Anonymous&sort=reliability&desc=true&pnum=%s' % uid
            html = self._fetchHtml(u)
            html = re.sub('\r|\n', '', html)
            rows = re.findall(pattern, html)
            for row in rows:
                m = re.findall(a, row)
                n = re.findall(b, row)
                proxies.append(m[0] + ":" + n[0])
                self.logger.debug(m[0] + ":" + n[0])
            uid = uid + 1
            if "{}#table'>{}".format(uid, uid + 1) not in html:
                break
        self._save_proxies(proxies)

    def proxzHttp(self):
        '''proxz.com'''
        proxies = []
        scriptpattern = re.compile('''<script type='text/javascript'>eval\(unescape\('([^']+)'\)\);</script>''')
        pattern = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>')
        for uid in range(10):
            u = 'http://www.proxz.com/proxy_list_high_anonymous_%s.html' % uid
            html = self._fetchHtml(u)
            scripts = re.findall(scriptpattern, html)
            if scripts:
                html = scripts[0]
                html = urllib2.unquote(html)
                searchs = re.findall(pattern, html)
                for g in searchs:
                    proxies.append(g[0] + ":" + g[1])
                    self.logger.debug(g[0] + ":" + g[1])
        self._save_proxies(proxies)

    def proxylistsHttp(self):
        '''proxylists.net'''
        dicpattern = '''<a href='/([a-zA-Z]+)_0\.html'>[^<]+</a><br/>'''
        scriptpattern = re.compile(
            '''<script type='text/javascript'>eval\(unescape\('([^']+)'\)\);</script><noscript>Please enable javascript</noscript></td><td>(\d+)</td><td>[Aa]nonymous</td>''')
        pattern = re.compile('(\d+\.\d+\.\d+\.\d+)')
        proxies = []
        html = self._fetchHtml('http://www.proxylists.net/countries.html')
        dics = re.findall(dicpattern, html)
        for dic in dics:
            bbb = set(proxies)
            proxies = list(bbb)
            uid = 0
            while True:
                u = 'http://www.proxylists.net/%s_%s_ext.html' % (dic, uid)
                html = self._fetchHtml(u)
                searchs = re.findall(scriptpattern, html)
                for g in searchs:
                    scripts = urllib2.unquote(g[0])
                    ips = re.findall(pattern, scripts)
                    proxies.append(ips[0] + ":" + g[1])
                    self.logger.debug(ips[0] + ":" + g[1])
                uid = uid + 1
                if "<a href='{}_{}_ext.html'>{}</a>".format(dic, uid, uid+1) not in html:
                    break
        self._save_proxies(proxies)

    def proxy_listen_deHttp(self):
        '''www.proxy-listen.de'''
        pattern = re.compile(
            '<tr class="proxyList[^"]+"><td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td><td>[^<]+</td><td>[12]</td>')
        key_pattern = re.compile('''name="fefefsfesf4tzrhtzuh" value="([^"]+)"''')
        pageurl = 'http://www.proxy-listen.de/Proxy/Proxyliste.html'
        html = self._fetchHtml(pageurl)
        keysearch = re.findall(key_pattern, html)
        ggfhgfjcfgds = keysearch[0]
        postdata = {
            'filter_port': '',
            'filter_http_gateway': '',
            'filter_http_anon': '',
            'filter_response_time_http': '',
            'fefefsfesf4tzrhtzuh': ggfhgfjcfgds,
            'filter_country': '',
            'filter_timeouts1': '30',
            'liststyle': 'info',
            'proxies': '300',
            'type': 'httphttps',
            'submit': 'Show'
        }

        pageid = 1
        proxies = []
        while True:
            html = self._fetchHtml(pageurl, data=postdata, referer=pageurl)
            html = re.sub('\r|\n', '', html)
            html = re.sub('<a[^>]+>', '', html)
            html = re.sub('</a>', '', html)
            searchs = re.findall(pattern, html)
            for g in searchs:
                proxies.append(g[0] + ':' + g[1])
                self.logger.debug(g[0] + ':' + g[1])
            pageid = pageid + 1
            if '''<input onclick="nextPage();" id="next_page" type="submit" value="next page" name="next"/>''' not in html:
                break
        self._save_proxies(proxies)

    def proxy_list_orgHttp(self):
        url = 'https://proxy-list.org/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p={}'
        pattern = re.compile("Proxy\('([^']+)'\)")
        proxies = []
        for i in range(1, 4):
            pageurl = url.format(i)
            html = self._fetchHtml(pageurl)
            searchs = re.findall(pattern, html)
            for g in searchs:
                p = base64.decodestring(g)
                proxies.append(p)
                self.logger.debug(p)
        self._save_proxies(proxies)

    def _validate_proxy(self, ip , port):
        url = 'http://gfw2.52yyh.com/hi.php'
        proxies = {'http': 'http://{}:{}'.format(ip, port)}
        html = self._fetchHtml(url, proxies=proxies, timeout=20)
        if html.strip() == ip:
            sql = 'update http set `lastcheck`=CURRENT_TIMESTAMP, `failtimes`=0 ' \
                  'where `ip`=%(ip)s and `port`=%(port)s'
        else:
            sql = 'update http set `lastcheck`=CURRENT_TIMESTAMP, `failtimes`=`failtimes`+1 ' \
                  'where `ip`=%(ip)s and `port`=%(port)s'
        self.db.execute(sql, {'ip': ip, 'port': port})

    def _query_proxy(self):
        sql = 'select `ip`, `port` from http ' \
              'where `failtimes`>5 ' \
              'or `lastcheck`<DATE_ADD(CURRENT_TIMESTAMP, INTERVAL -120 SECOND) or ISNULL(`lastcheck`) ' \
              'order by `lastcheck` limit 100'
        rows = self.db.fetchall(sql)
        jobs = [gevent.spawn(self._validate_proxy, row[0], int(row[1])) for row in rows]
        return jobs

    def fetch(self):
        while True:
            gevent.joinall([
                gevent.spawn(self.freeproxylistsHttp),
                gevent.spawn(self.freeproxylist),
                gevent.spawn(self.cnproxyHttp),
                gevent.spawn(self.ipcnorgHttp),
                gevent.spawn(self.samairruHttp),
                gevent.spawn(self.nntimeHttp),
                gevent.spawn(self.xroxyHttp),
                gevent.spawn(self.proxzHttp),
                gevent.spawn(self.proxylistsHttp),
                gevent.spawn(self.proxy_listen_deHttp),
                gevent.spawn(self.proxy_list_orgHttp),
            ])
            gevent.sleep(360)

    def check(self):
        while True:
            jobs = self._query_proxy()
            gevent.wait(jobs)
            gevent.sleep(3)

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
        monkey.patch_all()
        thread = gevent.spawn(func)
        thread.start()
        thread.join()