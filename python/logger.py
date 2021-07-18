#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging


baselog_file = "/var/log/test.log"

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s. %(filename)s:%(lineno)d %(levelname)s %(message)s',
                filename=baselog_file)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s. %(filename)s:%(lineno)d %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#logfile = "/var/log/test.debug.log"
#log = logging.FileHandler(logfile)
#log.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s. %(filename)s:%(lineno)d %(levelname)s %(message)s')
#log.setFormatter(formatter)
#logging.getLogger('').addHandler(log)

LOG = logging


if __name__ == '__main__':
    LOG.info("info")
    LOG.debug("debug")
