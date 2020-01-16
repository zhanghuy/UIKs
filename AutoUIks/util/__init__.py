import threading
import time
import os
import unittest
import util.proxyscript

from cases.pigai import CalculatorTest

def sing(num = 1):
    for i in range(num):
        print("sing%d" % i)
        os.system( 'mitmdump -s mitmproxyscript.py -p 8080')
        time.sleep(0.5)


def testcases(num = 1):
    for i in range(num):
        print("dancing%d" % i)
        a = CalculatorTest()
        a.setUp()
        a.test_plus()
        a.tearDown()


def main():
    """创建启动线程"""
    t_sing = threading.Thread(target=sing)
    t_testcases = threading.Thread(target=testcases)
    t_sing.start()
    time.sleep(5)
    t_testcases.start()


if __name__ == '__main__':
    main()


