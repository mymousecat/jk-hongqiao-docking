# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wdh
   date：          2020-03-03
-------------------------------------------------
   Change Activity:
                   2020-03-03:
-------------------------------------------------
"""


import json

if __name__ == '__main__':
    a = ['1','2','3']
    b = ['4','5']
    c = []
    c.extend(a)
    c.extend(b)
    print(c)