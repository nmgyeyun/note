#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
from collections import defaultdict


def datetime_now_convert():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_time(datetime_str):
    return time.mktime(time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))



