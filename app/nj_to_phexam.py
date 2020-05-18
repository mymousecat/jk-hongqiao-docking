# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     nj_to_phexam
   Description :   内镜结果到体检
   Author :       wdh
   date：          2020-05-18
-------------------------------------------------
   Change Activity:
                   2020-05-18:
-------------------------------------------------
"""

from . import appconfig
import logging
import re
import json
from .err import InvalidParamException
from jktj.jktj import loginByUserNamePwd,\
    tjAssert,\
    loginAssems,\
    loadExam,\
    getUserIdByRealName,\
    getDiseaseByName,\
    saveExamData
from jktj.tjsaveexam import initSaveExam,addElementResult,addDisease
from jktj.tjexception import TJException
# from .models import TJPacsResult

log = logging.getLogger(__name__)


def _get_opid(opName,auditName):
    auditName = auditName if auditName else opName  # 审核医生，如果审核医生为空，则使用报告医生

    log.info('获取到报告医生:{}  审核医生:{}'.format(opName, auditName))

    opId = getUserIdByRealName(opName, False, 'nj')

    log.info("获取报告医生id:{}  用户名:{}".format(opId, opName))

    if not auditName:
        raise TJException('没有发现有效的审核医生')

    auditId = getUserIdByRealName(auditName, False, 'nj')

    log.info("获取审核医生id:{}  用户名:{}".format(auditId, auditName))
    return opId, auditId


def _login():
    log.info('开始登录体检系统')
    r = loginByUserNamePwd(appconfig['JK_EXAM_USERNAME'], appconfig['JK_EXAM_PASSWORD'])
    tjAssert(r)
    log.info('体检系统登录成功')


def nj_to_exam(tjPacsResult,NJ_DEPARTMENT_ID):
    log.info('开始对内镜记录 id:{} 预约号:{} 检查部位:{}进行操作'.format(tjPacsResult.id,tjPacsResult.register_num,tjPacsResult.check_part))
    log.info('开始对诊断部位:{}进行分解...'.format(tjPacsResult.check_part))
    desc,order_id,assem_id = re.split(r'\^',tjPacsResult.check_part)
    if order_id is None or assem_id is None:
        raise InvalidParamException('无效的部位代码,{}'.format(tjPacsResult.check_part))
    log.info('获取到预约号:{}  项目组id:{}'.format(order_id,assem_id))
    log.info('开始检查操作类型:{}'.format(tjPacsResult.rec_type))
    _login()
    if tjPacsResult.rec_type == '1':
        log.info('开始登记...')
        tjAssert(loginAssems(order_id, assem_id, None))  # 为None的话，为当前的登录者进行操作
        log.info('预约号：{} 项目组：{}登入操作成功'.format(order_id, assem_id))
    elif tjPacsResult.rec_type == '2':
        log.info('开始保存体检结果...')
        msg = tjAssert(
            loadExam(dept=NJ_DEPARTMENT_ID, orderId=order_id, filterAssemIds=assem_id))

        exam = msg['msg']

        assem = exam['assems'][0]

        element = assem['elements'][0]

        # 初始化保存数据
        reporterId, confirmId = _get_opid(tjPacsResult.report_doctor,tjPacsResult.audit_doctor)

        log.info('获取到报告者id:{} 审核者id:{}'.format(reporterId, confirmId))

        saveExam = initSaveExam(exam, NJ_DEPARTMENT_ID, confirmId, reporterId)

        # 小项结果
        fs = {'others': tjPacsResult.check_diag}
        addElementResult(saveExam, exam=exam, opId=reporterId, **fs)
        # 项目结论
        log.info('获取结论...')
        writeSymbol = None
        diseaseCode = None

        dialogs = re.split(r'[\d]+\s*\.|[\d]+\s*、|\r\n',tjPacsResult.check_result)

        writeSymbol = None
        diseaseCode = None

        for diaglog in dialogs:
            diseaseCode = None
            if diaglog and diaglog.strip():
                if diaglog.find('无异常') >= 0 or diaglog.find('无明显异常') >=0: #默认小节
                    writeSymbol = '03'
                else:
                    result = getDiseaseByName(diaglog)
                    if result is None:
                        writeSymbol = '02'
                    else:
                        writeSymbol = '01'
                        diseaseCode = result['msg']['id']
                log.info("获取诊断方式:{},疾病名称:{},疾病id:{}".format(writeSymbol, diaglog, diseaseCode))
                addDisease(saveExam, exam=exam, deptId=NJ_DEPARTMENT_ID, opId=reporterId, writeSymbol=writeSymbol,
                           diseaseName=diaglog, diseaseCode=diseaseCode)
        # 开始提交分科结果
        examData = json.dumps(saveExam)
        log.info(examData)
        log.info('开始提交分科结果...')
        result = tjAssert(saveExamData(examData))
        log.info(result['msg'])











