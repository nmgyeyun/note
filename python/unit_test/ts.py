#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import unittest
from test_class import utCase
# from HTMLTestRunner import HTMLTestRunner


def report_text():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(utCase))

    with open('ut_report.txt', 'a') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)

def report_html():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(utCase))

    with open('ut_report.html', 'w') as f:
        runner = HTMLTestRunner(stream=f,
                                title='MathFunc Test Report',
                                description='generated by HTMLTestRunner.',
                                verbosity=2
                                )
        runner.run(suite)

def all_case():
    cases =  unittest.TestLoader().discover(os.getcwd())
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(cases)


if __name__ == '__main__':
    # report_html()
    # report_text()
    all_case()
