# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     utils
   Description :   请求及返回结果的工具集
   Author :       wdh
   date：          2020-03-06
-------------------------------------------------
   Change Activity:
                   2020-03-06:
-------------------------------------------------
"""

from suds.client import Client
import xmltodict
from .err import InvalidParamException
import datetime
from app import redis


webClient = None


def init(url):
    global webClient
    if webClient is None:
        webClient = Client(url=url)


def get_birth(now, age):
    return (now - datetime.timedelta(days=age * 365)).strftime('%Y-%m-%d')


def get_cert_type(exam_cert_type):
    """
    体检系统证件类型转换成平台类型
    :param exam_cert_type:
    :return:
    """
    # 体检系统证件类型，1 身份证 2 护照
    cert_type = None
    if exam_cert_type == '1':
        cert_type = '01'
    elif exam_cert_type == '2':
        cert_type = '03'
    elif exam_cert_type == '4':
        cert_type = '04'
    return cert_type


def get_sqh(sq_type):
    """
    获取申请号
    :sq_type 申请号的类型 JC LIS 等
    :return:
    """
    s = redis.incr('docking:sqh:{}'.format(sq_type))
    return '{}{:08d}'.format(sq_type, int(s))


def make_response(msg, ex=None):
    """
    生成回应的xml，本地的webservice使用
    :param msg:
    :param ex:
    :return:
    """
    r = {
        'RETURN': {
            'FHZTM': None,
            'FHXX': None
        }}
    if ex:
        r['RETURN']['FHXX'] = repr(ex)
        if hasattr(ex, 'errcode'):
            r['RETURN']['FHZTM'] = ex.errcode
        else:
            r['RETURN']['FHZTM'] = 500
    else:
        r['RETURN']['FHXX'] = msg
        r['RETURN']['FHZTM'] = 200
    return to_xml(r)


def check_params(params, must_exist):
    """
    检查参数的前效性，并将xml格式的参数转为字典类型返回
    :param params:
    :return:
    """
    param = xmltodict.parse(params)
    if not param.get(must_exist, None):
        raise InvalidParamException('获取到的参数无效，在获取到的XML中没有找到必须节点[{}]'.format(must_exist))
    return param


def queryAQMY(YLJGDM, BCYLJGDM):
    """

    :param YLJGDM:自己医疗机构代码
    :param YLJGMM:自己医疗机构登录密码
    :param BCYLJGDM:需要查询的医疗机构代码
    :return:
    """

    # r = webClient.queryAQMY(YLJGDM, YLJGMM, BCYLJGDM)
    pass


# def build_param(params_dict, is_required_token):
#     """
#     生成请求的参数
#     :param params_dict:
#     :param is_required_token:
#     :return:
#     """
#     r = {
#         'PARAMS': params_dict
#     }
#
#     return r

def to_xml(obj_dict):
    return xmltodict.unparse(obj_dict, full_document=True, pretty=True)


def get_init_dict():
    r = {

        'PARAMS': {}
    }
    return r


def build_lis(lis_assems_list, build_dict):
    """
    根据数据库返回的项目组结果，按平台要求，生成字典
    :param lis_assems_list:
    :return:
    """

    for assems in lis_assems_list:
        build_dict['PARAMS']['SJRQ'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        build_dict['PARAMS']['SQJGTM'] = assems.BARCODE_ID
        build_dict['PARAMS']['BRID'] = assems.ORDER_ID
        build_dict['PARAMS']['YWLSH'] = format('{}^{}'.format(assems.ORDER_ID, assems.BARCODE_ID))
        build_dict['PARAMS']['MZBZ'] = '3'
        build_dict['PARAMS']['JZKH'] = None
        build_dict['PARAMS']['KLX'] = '9'
        build_dict['PARAMS']['BRXM'] = assems.USERNAME
        build_dict['PARAMS']['BRXB'] = assems.SEX
        build_dict['PARAMS']['BRNL'] = assems.AGE
        build_dict['PARAMS']['NLDW'] = '岁'
        build_dict['PARAMS']['CSRQ'] = assems.BIRTHDAY.strftime('%Y-%m-%d') if assems.BIRTHDAY else get_birth(
            assems.INITIAL_TIME, assems.AGE)

        build_dict['PARAMS']['JZXH'] = assems.ORDER_ID
        build_dict['PARAMS']['JTZZ'] = assems.ADDRESS
        build_dict['PARAMS']['LXDH'] = assems.TELEPHONE
        build_dict['PARAMS']['ZJLX'] = get_cert_type(assems.CERT_TYPE)
        build_dict['PARAMS']['ZJHM'] = assems.CERT_ID
        build_dict['PARAMS']['JZRQ'] = None
        build_dict['PARAMS']['LCZD'] = None
        build_dict['PARAMS']['KDKS'] = assems.DEPARMENT
        build_dict['PARAMS']['BRBQ'] = None
        build_dict['PARAMS']['BRCH'] = None
        build_dict['PARAMS']['BBCJSJ'] = None
        build_dict['PARAMS']['BBLX'] = assems.SPECIMEN_TYPE_NAME
        build_dict['PARAMS']['SJYS'] = None
        build_dict['PARAMS']['BZ'] = None
        if build_dict['PARAMS'].get('FORMS') is None:
            build_dict['PARAMS']['FORMS'] = []

        child = {
            'FORM': {}
        }
        child['FORM']['YZID'] = None
        child['FORM']['SFXMDM'] = assems.ASSEM_CODE
        child['FORM']['SFXMMC'] = assems.ASSEM_NAME
        child['FORM']['XMDM'] = assems.ELEMENT_CODE
        child['FORM']['XMMC'] = assems.ELEMENT_NAME
        build_dict['PARAMS']['FORMS'].append(child)
