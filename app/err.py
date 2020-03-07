# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     err
   Description :
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""


class InvalidParamException(Exception):
    """
      XML输入异常
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 500

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class NotFoundException(Exception):
    """
      XML输入异常
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 404

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

