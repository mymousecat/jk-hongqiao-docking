# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     request_lis
   Description :   向LIS发送申请
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""

from .utils import build_lis, get_sqh, get_token, get_barcode_from_webservice, req_to_lis
from .db_op import get_assem_info_by_barcode
from .err import NotFoundException
import logging

log = logging.getLogger(__name__)


def request_to_lis(barcode, YLJGDM, YLJGMM, SYSDM, SQJGDM, build_dict):
    """
    通过样本号，向平台lis发出申请
    :param barcode:本医院条码号
    :param YLJGDM:本医院机构ID
    :param YLJGMM:本医院密码
    :param SYSDM:检验室分配给本医院的代码 上传的结构体里需要填入这个
    :param SQJGDM:申请机构代码 不知道这个干啥的
    :build_dict:要构建的字典，用来生成向lis的申请
    :return:
    """
    log.info('开始使用条码号为:[{}]在体检系统中进行查询，获取项目等信息...'.format(barcode))
    assems = get_assem_info_by_barcode(barcode)
    if len(assems) == 0:
        raise NotFoundException('条码号为:[{}]在体检系统中未找到项目信息'.format(barcode))
    log.info('条码号为：[{}]中，一共找到[{}]条项目信息'.format(barcode, len(assems)))
    log.info('开始拼接项目信息...')
    build_lis(assems, build_dict)
    log.info('开始补全发送的LIS信息...')
    build_dict['PARAMS']['YLJGDM'] = YLJGDM
    build_dict['PARAMS']['SYSDM'] = SYSDM
    build_dict['PARAMS']['SQJGDM'] = SQJGDM
    build_dict['PARAMS']['SQDH'] = get_sqh('LIS')
    build_dict['PARAMS']['TOKEN'] = get_token(SQJGDM, YLJGMM, SQJGDM)

    log.info('开始从平台获取条码号...')
    # zxtm = get_barcode_from_webservice(YLJGDM=YLJGDM,
    #                                    SQJGDM=SQJGDM,
    #                                    SYSDM=SYSDM,
    #                                    SQDH=build_dict['PARAMS']['SQDH'],
    #                                    BRID=build_dict['PARAMS']['BRID'],
    #                                    YWLSH=build_dict['PARAMS']['YWLSH'],
    #                                    MZBZ=build_dict['PARAMS']['MZBZ'],
    #                                    BBLX=build_dict['PARAMS']['BBLX'],
    #                                    TOKEN=build_dict['PARAMS']['TOKEN']
    #                                    )
    # log.info('从平台获取到平台条码号:{}'.format(zxtm))
    # build_dict['PARAMS']['ZXJGTM'] = zxtm
    log.info('申请的lis数据为:{}'.format(build_dict))
    req_to_lis(build_dict)
