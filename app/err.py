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


class SkipDelFlagException(Exception):
    """
      跳过删除标记的记录
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 404

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class Response500Exception(Exception):
    """
      500: 系统错误异常
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 500

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class Response501Exception(Exception):
    """
      501: 业务错误
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 501

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class Response401Exception(Exception):
    """
      401: 未授权，无token
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 401

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class Response403Exception(Exception):
    """
      403: 无权限, 有token
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 403

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class ResponseUnkownException(Exception):
    """
          返回的未知错误
    """

    def __init__(self, msg):
        self.msg = msg
        self.errcode = 'unkown'

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)
