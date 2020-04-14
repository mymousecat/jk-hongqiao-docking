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
from jktj.jktj import loginByUserNamePwd, tjAssert, getUserIdByRealName, loginAssems
from jktj.tjexception import TJException
from . import appconfig

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
        'is_success': True if ex is None else ex,
        'ex': ex
    }

    r_list.append(r_dict)


def _get_opid(lis_results_dict):
    opName = lis_results_dict.get('JYYS', None)  # 报告医生
    auditName = lis_results_dict.get('SHYS', None) if lis_results_dict.get('SHYS',
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
            log.info('预约号：{} 项目组：{}登入操作失败!'.format(orderId, assemId))
            log.error(e)
    elif dockingPacsFollowing.ZTBZ == '4':
        try:
            pass
        except Exception as e:
            pass
