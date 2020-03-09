# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     request_pacs
   Description :
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""

from .utils import build_pacs, get_sqh, get_token, req_to_pacs
from .db_op import get_assem_info_by_order_assem_id
from .err import NotFoundException
import logging

log = logging.getLogger(__name__)


def request_to_pacs(order_id, assem_id, YLJGDM, YLJGMM, SQJGDM, build_dict):
    """
    通过样本号，向平台lis发出申请
    :param order_id:本次预约号
    :param assem_id:项目组ID
    :param YLJGDM:本医院机构ID
    :param YLJGMM:本医院密码
    :param SQJGDM:申请机构代码 不知道这个干啥的
    :build_dict:要构建的字典，用来生成向lis的申请
    :return:
    """

    log.info('开始使用预约号为:[{}]  项目组ID为:[{}] 在体检系统中进行查询，获取项目等信息...'.format(order_id, assem_id))
    assems = get_assem_info_by_order_assem_id(order_id, assem_id)
    if len(assems) == 0:
        raise NotFoundException('条码号为:[{}] 项目组ID为:[{}] 在体检系统中未找到项目信息'.format(order_id, assem_id))
    log.info('开始拼接项目信息...')
    build_pacs(assems, build_dict)
    log.info('开始补全发送的PACS信息...')
    build_dict['PARAMS']['YLJGDM'] = YLJGDM
    build_dict['PARAMS']['SQJGDM'] = SQJGDM
    build_dict['PARAMS']['SQDH'] = get_sqh('PACS')
    build_dict['PARAMS']['TOKEN'] = get_token(YLJGDM, YLJGMM, SQJGDM)
    log.info('申请的pacs数据为:{}'.format(build_dict))
    request_to_pacs(build_dict)
