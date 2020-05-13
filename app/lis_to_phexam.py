# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     lis_to_phexam
   Description :   LIS到体检系统
   Author :       wdh
   date：          2020-04-02
-------------------------------------------------
   Change Activity:
                   2020-04-02:
-------------------------------------------------
"""

import logging

from . import appconfig

from .db_op import get_assems_by_barcode_id

from .err import NotFoundException

from jktj.jktj import loginByUserNamePwd, loginAssems, tjAssert, getUserIdByRealName, loadExam, saveLisExamData

from jktj.tjexception import TJException

from .utils import get_init_dict, build_lis_report, get_token, get_report_no_from_lis, build_lis_report_results, \
    get_report_result_from_lis

import re

import json

log = logging.getLogger(__name__)


def _login():
    log.info('开始登录体检系统')
    r = loginByUserNamePwd(appconfig['JK_EXAM_USERNAME'], appconfig['JK_EXAM_PASSWORD'])
    tjAssert(r)
    log.info('体检系统登录成功')


def _appen_msg(r_list, orderId, assems, assem_name, op, msg, ex, lis_result, barcode):
    r_dict = {
        'orderId': orderId,
        'assems': assems,
        'assem_name': assem_name,
        'op': op,
        'msg': msg if ex is None else repr(ex),
        'is_success': True if ex is None else False,
        'ex': ex,
        'lis_result': lis_result,
        'barcode': barcode
    }

    r_list.append(r_dict)


def _tojson(obj):
    return json.dumps(obj, ensure_ascii=False, indent=3)


def _get_opid(opName, auditName):
    # opName = lis_results_dict.get('JYYS', None)  # 报告医生
    # auditName = lis_results_dict.get('SHYS', None) if lis_results_dict.get('SHYS',
    #                                                                        None) is not None else opName  # 审核医生，如果审核医生为空，则使用报告医生

    log.info('获取到报告医生:{}  审核医生:{}'.format(opName, auditName))

    opId = getUserIdByRealName(opName, False, 'lis')

    log.info("获取报告医生id:{}  用户名:{}".format(opId, opName))

    if not auditName:
        raise TJException('没有发现有效的审核医生')

    auditId = getUserIdByRealName(auditName, False, 'lis')

    log.info("获取审核医生id:{}  用户名:{}".format(auditId, auditName))
    return opId, auditId


def lis_to_phexam(lisDepartment, dockingLisFollowing, SQJGMM):
    """
    LIS到体检系统登入状态、LIS结果导入
    :param dockingLisFollowing:
    :return:
    """

    r_list = []

    ll = []

    log.info('开始查询本样本号所做的项目....')
    assems = get_assems_by_barcode_id(dockingLisFollowing.ZXTM)
    str_assems = ','.join(assems)
    if len(assems) == 0:
        raise NotFoundException('在检检系统中，未发现条码号为:{}的任何项目组'.format(dockingLisFollowing.ZXTM))

    if not dockingLisFollowing.BRID:
        raise TJException('不存在的预约号')

    if dockingLisFollowing.ZTBZ == '2':  # 表示样本号已经在LIS中登记
        log.info('开始对预约号:{}  项目组列表:{}  进行登入操作'.format(dockingLisFollowing.BRID, str_assems))
        try:
            _login()
            loginAssems(dockingLisFollowing.BRID, str_assems, None)  # 为None的话，为当前的登录者进行操作
            log.info('项目组登入操作成功')
            _appen_msg(r_list=r_list, orderId=dockingLisFollowing.BRID, assems=str_assems, assem_name=None, op='登入',
                       msg='登入成功', ex=None, lis_result=None,
                       barcode=dockingLisFollowing.ZXTM)
        except Exception as e:
            _appen_msg(r_list, dockingLisFollowing.BRID, str_assems, None, '登入', None, e, None,
                       dockingLisFollowing.ZXTM)

    elif dockingLisFollowing.ZTBZ == '3':  # 表示报告已经完成
        try:
            log.info('开始从平台中，获取报告信息...')
            build_dict = get_init_dict()
            build_lis_report(dockingLisFollowing, build_dict)
            build_dict['PARAMS']['TOKEN'] = get_token(dockingLisFollowing.SQJGDM, SQJGMM, dockingLisFollowing.SQJGDM)
            report_nos = get_report_no_from_lis(build_dict)
            if len(report_nos) == 0:
                raise Exception('没有获取到报告编号')

            for report_no in report_nos:
                log.info('使用报告编码:{}查询项目结果'.format(report_no))

                req_results_dict = get_init_dict()

                build_lis_report_results(dockingLisFollowing, report_no, req_results_dict)

                req_results_dict['PARAMS']['TOKEN'] = get_token(dockingLisFollowing.SQJGDM, SQJGMM,
                                                                dockingLisFollowing.SQJGDM)

                lis_results = get_report_result_from_lis(req_results_dict)['Results']['Result']

                # 获取到检验医生和审核医生
                opName = lis_results.get('JYYS', None)  # 报告医生
                auditName = lis_results.get('SHYS', None) if lis_results.get('SHYS',
                                                                             None) is not None else opName  # 审核医生，如果审核医生为空，则使用报告医生

                result_dict_list = lis_results['ItemResultList']['ItemResult']

                if isinstance(result_dict_list, list):
                    for result in result_dict_list:
                        result['JYYS'] = opName
                        result['SHYS'] = auditName
                        ll.append(result)
                else:
                    result_dict_list['JYYS'] = opName
                    result_dict_list['SHYS'] = auditName
                    ll.append(result_dict_list)

            # 以lis项目id为key，建立字典
            lis_results_map = {}
            lis_results_set = set()

            for result in ll:
                key = result['XMBM']
                lis_results_map[key] = result
                lis_results_set.add(key)

            log.info('获取到lis数据的对照码集合为:{}'.format(lis_results_set))

            _login()

            assemName = None

            for assemId in assems:
                try:
                    log.info('开始循环获取预约号:{}的项目组id:{}的体检信息'.format(dockingLisFollowing.BRID, assemId))
                    msg = tjAssert(
                        loadExam(dept=lisDepartment, orderId=dockingLisFollowing.BRID, filterAssemIds=assemId))

                    exam = msg['msg']

                    assem = exam['assems'][0]

                    elements = assem['elements']

                    # 项目组名称
                    assemName = assem['assemName']

                    log.info('获取的体检系统的项目名称为:{}'.format(assemName))

                    # 使用外键组成项目字典
                    examElementDict = {}
                    examElementSet = set()

                    for element in elements:
                        extCode = element['extSysControlCode']

                        if not extCode:
                            raise TJException('项目名：{} 的系统对照为空'.format(element['elementName']))

                        # 开始分割项目对照码，一个小项，可以有多个对照码，使用,，|^，进行分割
                        keys = re.split(r',|，|\^|\|', extCode)
                        for key in keys:
                            if key:
                                code = key.strip()
                                if code:
                                    examElementDict[code] = element
                                    examElementSet.add(code)

                    log.info('获取到体检数据的对照码集合为:{}'.format(examElementSet))

                    # 计算项目编码的合集
                    both_set = set.intersection(examElementSet, lis_results_set)

                    log.info('得到的交集为:{}'.format(both_set))

                    # 开始对小项进行标记
                    for code in both_set:
                        examElementDict[code]['bingo'] = True

                    errMsgs = []

                    log.info('开始检查哪些项目，在HIS中没有结果...')

                    for element in elements:
                        if 'bingo' not in element.keys():
                            errMsg = '在LIS提供的项目列表中，未发现项目id:{} 项目名:{} 项目对照:{}的项目'.format(element['elementId'],
                                                                                        element['elementName'],
                                                                                        element['extSysControlCode'])
                            errMsgs.append(errMsg)

                    if len(errMsgs) > 0:
                        raise TJException(';'.join(errMsgs))

                    log.info('开始生成LIS体检项目...')

                    # sampleOpId, opId = _get_opid(lis_results)

                    lisDatas = {

                        'orderId': dockingLisFollowing.BRID,
                        'elementAssemId': assemId,
                        'departmentId': lisDepartment,
                        'sampleOpId': None,  # 报告人
                        'opId': None,  # 审核人
                        'items': []
                    }

                    sampleOpId = None
                    opId = None

                    isGetDoct = True

                    for code in both_set:
                        examElement = examElementDict[code]

                        hisLisElement = lis_results_map[code]

                        if isGetDoct:  # 开始获取医生,只取一次
                            sampleOpId, opId = _get_opid(hisLisElement.get('JYYS', None),
                                                         hisLisElement.get('SHYS', None))
                            lisDatas['sampleOpId'] = sampleOpId
                            lisDatas['opId'] = opId

                        lisElement = {}
                        lisElement['elementId'] = examElement['elementId']
                        lisElement['checkElementResult'] = hisLisElement.get('JCJG', None)

                        lisElement['ferenceLower'] = 0

                        lisElement['ferenceUpper'] = 0

                        # 参考范围,使用新版的参考范围
                        lisElement['showFerence'] = hisLisElement.get('CKFW', None)

                        lisElement['unit'] = hisLisElement.get('JLDW', None)

                        lisElement['resultType'] = examElement['resultType']
                        lisElement['referenceType'] = '1'  # e['refType']

                        # 危机值的标识？
                        lisElement['criticalValuesSymbol'] = hisLisElement.get('WJZBZ', None)

                        # SUM_JUDGE_TYPE ，项目异常下小结判断：0表示使用体检系统判断业务，1表示使用外接系统根据positiveSymbol判断

                        lisElement['sumJudgeType'] = 1

                        ycts = hisLisElement.get('YCTS', None)

                        resultType = examElement['resultType']

                        lisElement['positiveSymbol'] = ''

                        if resultType == '1':  # 数值类值
                            if ycts == '3':
                                lisElement['positiveSymbol'] = '高'
                            elif ycts == '4':
                                lisElement['positiveSymbol'] = '低'
                        elif resultType == '2':  # 文本类型
                            if ycts != '1':
                                lisElement['positiveSymbol'] = lisElement['checkElementResult']  # 非正常值的话，这里写检查结果

                        lisDatas['items'].append(lisElement)
                        isGetDoct = False

                    log.info('开始上传LIS结果数据...')

                    examData = json.dumps(lisDatas, ensure_ascii=False)
                    log.info(examData)

                    log.info("开始保存LIS结果....")
                    result = tjAssert(saveLisExamData(examData))
                    log.info(result['msg'])
                    _appen_msg(r_list, dockingLisFollowing.BRID, assemId, assemName, 'LIS结果传输', 'LIS结果传输成功',
                               None, _tojson(ll), dockingLisFollowing.ZXTM)
                except Exception as e:
                    _appen_msg(r_list, dockingLisFollowing.BRID, assemId, assemName, 'LIS结果传输', None,
                               e, _tojson(ll), dockingLisFollowing.ZXTM)

        except Exception as e:
            _appen_msg(r_list, dockingLisFollowing.BRID, str_assems, None, 'LIS结果传输', None,
                       e, _tojson(ll), dockingLisFollowing.ZXTM)

    return r_list
