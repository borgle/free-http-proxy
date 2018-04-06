#!/usr/bin/env python
# coding:utf-8

__version__ = '1.0.0'

import logging.config
import multiprocessing
import sys
import yaml

import bottle
from beaker.middleware import SessionMiddleware
from setting import Config
from controller import *


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


if __name__ == '__main__':
    with open('logging.yaml', 'rt') as f:
        yml = yaml.load(f.read())
        logging.config.dictConfig(yml)
    if len(sys.argv) < 2:
        host, port = '127.0.0.1', 8082
    else:
        host, _, port = sys.argv[1].rpartition(':')
    logging.info('this web application serving at %s:%s', host, port)
    bottle.TEMPLATE_PATH.insert(0, './templates')
    app = SessionMiddleware(bottle.default_app(),
                            config = Config.SessionOptions,
                            environ_key=Config.SessionOptions['session.key'])
    bottle.run(app=app, host=host, port=port, reloader=True, debug=True)


