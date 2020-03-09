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
from .err import InvalidParamException, \
    Response401Exception, \
    Response403Exception, \
    Response500Exception, \
    Response501Exception, \
    ResponseUnkownException
import datetime
from app import redis, app

lis_client = None
pacs_client = None
security_client = None


def _get_lis_client():
    global lis_client
    if lis_client is None:
        lis_client = Client(app.config['PLAT_LIS_URL'])
    return lis_client


def _get_pacs_client():
    global pacs_client
    if pacs_client is None:
        pacs_client = Client(app.config['PLAT_PACS_URL'])
    return pacs_client


def _get_security_client():
    global security_client
    if security_client is None:
        security_client = Client(app.config['PLAT_SECURITY_URL'])
    return security_client


def _get_birth(now, age):
    return (now - datetime.timedelta(days=age * 365)).strftime('%Y-%m-%d')


def _get_cert_type(exam_cert_type):
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


def _get_jclx(department_id):
    """
    通过科室id获取需要检查的类型
    :param department_id:
    :return:
    01计算机X线断层摄影[CT]
    02核磁共振成像[MR]
    03数字减影血管造影[DSA]
    04普通X光摄影[X-Ray]
    05特殊X光摄影[X-Ray]
    06超声检查[US]
    07病理检查[Microscopy]
    08內窥镜检查[ES]
    09核医学检查[NM]
    10其他检查[OT]
    11心电检查
    12 PETME
    13 PETCT
    备注：目前影像使用(MG、MR、PETMR、PETCT、CT、DX 、US)
    """
    if department_id == 5:
        return '06'
    elif department_id == 6:
        return '04'
    elif department_id == 20:
        return '01'
    elif department_id == 21:
        return '02'
    else:
        return None


def _parse_response(r, field=None):
    """
    解析webservice返回的xml结果
    :param r:输入的xml参数
    :param field:返回的字段的值
    :return:
    """
    d = xmltodict.parse(r)
    r_code = d['RETURN']['FHZTM']
    r_msg = d['RETURN']['FHXX']
    if r_code != '200':
        if r_code == '500':
            raise Response500Exception(r_msg)
        elif r_code == '501':
            raise Response501Exception(r_msg)
        elif r_code == '401':
            raise Response401Exception(r_msg)
        elif r_code == '403':
            raise Response403Exception(r_msg)
        else:
            raise ResponseUnkownException(r_msg)
    else:
        if field:
            return d['RETURN'][field]
        else:
            return d['RETURN']


def _get_token_by_webservice(YLJGDM, YLJGMM, BCYLJGDM):
    """
    从webservice获取token
    :param YLJGDM: 
    :param YLJGMM: 
    :param BCYLJGDM: 
    :return: 
    """""
    req = get_init_dict()
    req['PARAMS']['YLJGDM'] = YLJGDM
    req['PARAMS']['YLJGMM'] = YLJGMM
    req['PARAMS']['BCYLJGDM'] = BCYLJGDM
    client = _get_security_client()
    return _parse_response(client.queryAQMY(to_xml(req)), 'TOKEN')


def _get_expire_seconds():
    """
    获取过期的秒数
    :return:
    """
    now = datetime.datetime.now()
    max = datetime.datetime.combine(now.today(), now.time().max)
    return (max - now).seconds


def get_sqh(sq_type):
    """
    获取申请号
    :sq_type 申请号的类型 JC LIS 等
    :return:
    """
    s = redis.incr('docking:sqh:{}'.format(sq_type))
    return '{}{:08d}'.format(sq_type, int(s))


def get_token(YLJGDM, YLJGMM, BCYLJGDM):
    """
    获取token
    :param YLJGDM: 自己医疗机构代码
    :param YLJGMM: 自己医疗机构代码
    :param BCYLJGDM: 需要查询的医疗机构代码
    :return:获取到的token
    """
    redis_key = 'docking:token:{}:{}'.format(YLJGDM, BCYLJGDM)
    token = redis.get(redis_key)
    if not token:
        # 如果没有访问到密码,则通过webservice访问
        token = _get_token_by_webservice(YLJGDM, YLJGMM, BCYLJGDM)
        redis.set(redis_key, token, ex=_get_expire_seconds())
    return token


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


def to_xml(obj_dict):
    return xmltodict.unparse(obj_dict, full_document=True, pretty=True, short_empty_elements=True)


def get_init_dict():
    """
    生成初始化的请求字典
    :return:
    """
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
        build_dict['PARAMS']['CSRQ'] = assems.BIRTHDAY.strftime('%Y-%m-%d') if assems.BIRTHDAY else _get_birth(
            assems.INITIAL_TIME, assems.AGE)

        build_dict['PARAMS']['JZXH'] = assems.ORDER_ID
        build_dict['PARAMS']['JTZZ'] = assems.ADDRESS
        build_dict['PARAMS']['LXDH'] = assems.TELEPHONE
        build_dict['PARAMS']['ZJLX'] = _get_cert_type(assems.CERT_TYPE)
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


def build_pacs(pacs_assem_list, build_dict):
    """
    构建PACS请求所要求的结构体
    :param pacs_assem_list:
    :param build_dict:
    :return:
    """
    for assems in pacs_assem_list:
        build_dict['PARAMS']['KDRQ'] = assems.ARRIVAL_DATE.strftime('%Y-%m-%d %H:%M:%S')
        build_dict['PARAMS']['KDYS'] = None
        build_dict['PARAMS']['BRID'] = assems.ORDER_ID
        build_dict['PARAMS']['YWLSH'] = format('{}^{}'.format(assems.ORDER_ID, assems.ELEMENT_ASSEM_ID))
        build_dict['PARAMS']['MZBZ'] = '3'
        build_dict['PARAMS']['JZKH'] = None
        build_dict['PARAMS']['KLX'] = '9'
        build_dict['PARAMS']['BRXM'] = assems.USERNAME
        build_dict['PARAMS']['BRXB'] = assems.SEX
        build_dict['PARAMS']['BRNL'] = assems.AGE
        build_dict['PARAMS']['NLDW'] = '岁'
        build_dict['PARAMS']['CSRQ'] = assems.BIRTHDAY.strftime('%Y-%m-%d') if assems.BIRTHDAY else _get_birth(
            assems.INITIAL_TIME, assems.AGE)
        build_dict['PARAMS']['JTZZ'] = assems.ADDRESS
        build_dict['PARAMS']['LXDH'] = assems.TELEPHONE
        build_dict['PARAMS']['ZJLX'] = _get_cert_type(assems.CERT_TYPE)
        build_dict['PARAMS']['ZJHM'] = assems.CERT_ID
        build_dict['PARAMS']['JZRQ'] = build_dict['PARAMS']['KDRQ']
        build_dict['PARAMS']['LCZD'] = None
        build_dict['PARAMS']['KDKS'] = assems.DEPARMENT
        build_dict['PARAMS']['BRBQ'] = None
        build_dict['PARAMS']['BRCH'] = None
        build_dict['PARAMS']['JCLX'] = _get_jclx(assems.DEPARTMENT_ID)
        build_dict['PARAMS']['MZBS'] = None

        if build_dict['PARAMS'].get('FORMLISTS') is None:
            build_dict['PARAMS']['FORMLISTS'] = []

        child = {
            'FORMLIST': {}
        }

        child['FORMLIST']['XMDM'] = assems.ASSEM_CODE
        child['FORMLIST']['JCMC'] = assems.ASSEM_NAME
        child['FORMLIST']['JCBW'] = assems.ELEMENT_NAME
        child['FORMLIST']['BWBM'] = assems.ELEMENT_CODE


def req_to_lis(req_lis_dict):
    """
    向平台发出检验申请
    :param req_lis_dict:
    :return:
    """
    res = _get_lis_client().applicationFrom(to_xml(req_lis_dict))
    _parse_response(res)


def req_to_pacs(req_pacs_dict):
    """
    向平台发出pacs申请
    :param req_pacs_dict:
    :return:
    """
    res = _get_pacs_client().pacsApplicationFrom(to_xml(req_pacs_dict))
    _parse_response(res)


def get_barcode_from_webservice(YLJGDM, SQJGDM, SYSDM, SQDH, BRID, YWLSH, MZBZ, BBLX, TOKEN):
    """
    从平台获取平台条码号
    :param YLJGDM:自己医疗机构代码
    :param SQJGDM:申请机构代码
    :param SYSDM:检验分配给各家机构的代码
    :param SQDH:医院内部唯一号码
    :param BRID:病人唯一号/档案号
    :param YWLSH:门诊检验单则是医生就诊流水号，住院为住院流水号
    :param MZBZ:门诊住院标志
    :param BBLX:标本类型
    :param TOKEN:
    :param build_dict:
    :return:
    """
    r = get_init_dict()
    r['PARAMS']['YLJGDM'] = YLJGDM
    r['PARAMS']['SQJGDM'] = SQJGDM
    r['PARAMS']['SYSDM'] = SYSDM
    r['PARAMS']['SQDH'] = SQDH
    r['PARAMS']['BRID'] = BRID
    r['PARAMS']['YWLSH'] = YWLSH
    r['PARAMS']['MZBZ'] = MZBZ
    r['PARAMS']['BBLX'] = BBLX
    r['PARAMS']['TOKEN'] = TOKEN
    req = to_xml(r)
    res = _get_lis_client().getLisJytm(req)
    res_data = _parse_response(res)
    # 开始解析返回数据中的条码
    barcodes = res_data['Results']['BarCode']
    ll = None
    if isinstance(barcodes, list):
        ll = barcodes
    else:
        ll = [barcodes]
    # 由于业务的需要，这里只返回第一个
    return ll[0]['JYTM']
