#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

# 用于测试的类
class TestClass(object):
    def add(self, x, y):
        return x + y

    def is_string(self, s):
        return type(s) == str

    def raise_error(self):
        raise KeyError("test.")

# 测试用例
class utCase(unittest.TestCase):
    def setUp(self):
        self.test_class = TestClass()

    @unittest.skip("Skip test.")
    def test_add_5_5(self):
        self.assertEqual(self.test_class.add(5, 5), 10)

    def test_bool_value(self):
        self.assertTrue(self.test_class.is_string("hello world!"))

    def test_raise(self):
        self.assertRaises(KeyError, self.test_class.raise_error)

    def tearDown(self):
        del self.test_class

if __name__ == "__main__":
    unittest.main()
