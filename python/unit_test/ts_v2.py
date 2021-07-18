#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import unittest
from unittestreport import TestRunner


if __name__ == '__main__':
    # 第一步：加载测试套件
    suite1 = unittest.defaultTestLoader.discover(os.getcwd())
    # 第二步：创建运行对象，传入测试套件
    runner = TestRunner(suite1)
    # 第三步：执行测试
    runner.run()
