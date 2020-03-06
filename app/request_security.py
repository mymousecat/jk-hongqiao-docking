# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     request_security
   Description :
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""

from suds.client import Client

webClient = None


def init(url):
    global webClient
    if webClient is None:
        webClient = Client(url=url)


def queryAQMY(YLJGDM, YLJGMM, BCYLJGDM):
    """

    :param YLJGDM:自己医疗机构代码
    :param YLJGMM:自己医疗机构登录密码
    :param BCYLJGDM:需要查询的医疗机构代码
    :return:
    """

    r = webClient.queryAQMY(YLJGDM, YLJGMM, BCYLJGDM)
