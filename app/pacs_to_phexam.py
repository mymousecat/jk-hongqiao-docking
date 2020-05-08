# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     pacs_to_phexam
   Description :
   Author :       wdh
   date：          2020-04-14
-------------------------------------------------
   Change Activity:
                   2020-04-14:
-------------------------------------------------
"""
import logging
import re
from .err import InvalidParamException
from jktj.jktj import loginByUserNamePwd, \
    tjAssert, \
    getUserIdByRealName, \
    loginAssems, \
    loadExam, \
    getDiseaseByName, \
    saveExamData
from jktj.tjsaveexam import initSaveExam, addElementResult, addDisease

from jktj.tjexception import TJException
from .db_op import get_department_by_assem_id
from . import appconfig
from .utils import get_init_dict, get_token, build_pacs_report_result, get_report_result_from_pacs
import json

log = logging.getLogger(__name__)


def _login():
    log.info('开始登录体检系统')
    r = loginByUserNamePwd(appconfig['JK_EXAM_USERNAME'], appconfig['JK_EXAM_PASSWORD'])
    tjAssert(r)
    log.info('体检系统登录成功')


def _appen_msg(r_list, orderId, assems, assem_name, op, msg, ex):
    r_dict = {
        'orderId': orderId,
        'assems': assems,
        'assem_name': assem_name,
        'op': op,
        'msg': msg if ex is None else repr(ex),
        'is_success': True if ex is None else False,
        'ex': ex
    }

    r_list.append(r_dict)


def _get_opid(pacs_results_dict):
    opName = pacs_results_dict.get('BGYSXM', None)  # 报告医生
    auditName = pacs_results_dict.get('SHRXM', None) if pacs_results_dict.get('BGYSXM',
                                                                              None) is not None else opName  # 审核医生，如果审核医生为空，则使用报告医生

    log.info('获取到报告医生:{}  审核医生:{}'.format(opName, auditName))

    opId = getUserIdByRealName(opName, False, 'pacs')

    log.info("获取报告医生id:{}  用户名:{}".format(opId, opName))

    if not auditName:
        raise TJException('没有发现有效的审核医生')

    auditId = getUserIdByRealName(auditName, False, 'pacs')

    log.info("获取审核医生id:{}  用户名:{}".format(auditId, auditName))
    return opId, auditId


def pacs_to_phexam(dockingPacsFollowing, SQJGMM):
    r_list = []
    log.info('开始拆分医院内流水号:{}'.format(dockingPacsFollowing.YWLSH))
    (orderId, assemId) = re.split(r'\^', dockingPacsFollowing.YWLSH)
    log.info('获取到预约号为:{} 项目组id为:{}'.format(orderId, assemId))
    if orderId is None or assemId is None:
        raise InvalidParamException('获取到的预约号或项目组无效')
    if dockingPacsFollowing.ZTBZ == '1':
        log.info('开始登记预约号：{} 项目组：{} 的记录'.format(orderId, assemId))
        try:
            _login()
            loginAssems(orderId, assemId, None)  # 为None的话，为当前的登录者进行操作
            log.info('预约号：{} 项目组：{}登入操作成功'.format(orderId, assemId))
            _appen_msg(r_list, orderId, assemId, None, '登入', '登入成功', None)
        except Exception as e:
            _appen_msg(r_list, orderId, assemId, None, '登入', None, e)
            log.error('预约号：{} 项目组：{}登入操作失败!'.format(orderId, assemId))
            log.error(e)
    elif dockingPacsFollowing.ZTBZ == '4':
        assemName = None
        try:
            log.info('开始获取预约号：{} 项目组id：{}的结果信息'.format(orderId, assemId))
            log.info('开始通过项目组id：{}来获取科室id'.format(assemId))
            departmentId = get_department_by_assem_id(assemId)
            if departmentId is None:
                raise TJException('项目组:{}在体检中未找到科室'.format(assemId))
            log.info('开始获取报告列表...')
            build_dict = get_init_dict()
            build_pacs_report_result(dockingPacsFollowing, build_dict)
            build_dict['PARAMS']['TOKEN'] = get_token(dockingPacsFollowing.SQJGDM, SQJGMM, dockingPacsFollowing.SQJGDM)
            pacs_results = get_report_result_from_pacs(build_dict)
            log.info('获取到PACS的结果为:{}'.format(pacs_results))
            pacs_result_dict = pacs_results['FORMLISTS']['FORMLIST']

            # 检查结果阴阳性,0未做1阴性2阳性
            yybz = pacs_result_dict.get('YYBZ', None)
            yxbx = pacs_result_dict.get('YXBX', None)
            jcts = pacs_result_dict.get('JCTS', None)

            log.info('从报告获取到阳性标识：{} 影像表现:{} 检查提示：{} '.format(yybz, yxbx, jcts))

            log.info('从体检系统中获取体检结果...')

            _login()

            msg = tjAssert(
                loadExam(dept=departmentId, orderId=orderId, filterAssemIds=assemId))

            exam = msg['msg']

            assem = exam['assems'][0]

            element = assem['elements'][0]

            # 项目组名称
            assemName = assem['assemName']

            log.info('获取到项目组名:{}'.format(assemName))

            # 初始化保存数据
            reporterId, confirmId = _get_opid(pacs_result_dict)
            log.info('获取到报告者id:{} 审核者id:{}'.format(reporterId, confirmId))
            saveExam = initSaveExam(exam, departmentId, confirmId, reporterId)

            # 小项结果
            fs = {'others': yxbx}
            addElementResult(saveExam, exam=exam, opId=reporterId, **fs)

            # 项目结论
            log.info('获取结论...')
            writeSymbol = None
            diseaseCode = None
            if yybz == '2':  # 阳性
                result = getDiseaseByName(jcts)
                if result is None:
                    writeSymbol = '02'
                else:
                    writeSymbol = '01'
                    diseaseCode = result['msg']['id']
            elif yybz == '1':  # 阴性
                writeSymbol = '03'

            log.info("获取诊断方式:{},疾病名称:{},疾病id:{}".format(writeSymbol, jcts, diseaseCode))

            addDisease(saveExam, exam=exam, deptId=departmentId, opId=reporterId, writeSymbol=writeSymbol,
                       diseaseName=jcts, diseaseCode=diseaseCode)

            # 开始提交分科结果
            examData = json.dumps(saveExam)
            log.info(examData)
            log.info('开始提交分科结果...')
            result = tjAssert(saveExamData(examData))
            log.info(result['msg'])

            _appen_msg(r_list, orderId, assemId, assemName, 'PACS结果传输', '体检结果接收成功', None)

        except Exception as e:
            _appen_msg(r_list, orderId, assemId, assemName, 'PACS结果传输', repr(e), e)
            log.error('预约号：{} 项目组：{}获取PACS结果失败'.format(orderId, assemId))
            log.error(e)
    return r_list
