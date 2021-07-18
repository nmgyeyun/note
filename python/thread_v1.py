#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import multiprocessing


class MyTask(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        super(MyTask, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def run(self):
        self.func(*self.args, **self.kwargs)


def mount_all(self):
    tasks = []
    for value in values():
        try:
            task = MyTask(func1, value)
            tasks.append(task)
            task.start()
        except Exception as e:
            log.error(str(e))

    for task in tasks:
        task.join()


def func1(value):
    log.debug("value %s" % value)
