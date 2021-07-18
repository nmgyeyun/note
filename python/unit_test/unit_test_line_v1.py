#!/usr/bin/python3
# coding=utf-8

import line_profiler
import unittest
import re
import time
import sys





class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        time.sleep(3)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        time.sleep(3)
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':

    profile = line_profiler.LineProfiler(unittest.main) 
    profile.enable()  # 开始分析
    
    unittest.main()
    
    profile.disable()  # 停止分析
    profile.print_stats(sys.stdout) 
    
