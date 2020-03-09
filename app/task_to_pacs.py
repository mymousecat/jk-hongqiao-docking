# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task_to_pacs
   Description :
   Author :       wdh
   date：          2020-03-09
-------------------------------------------------
   Change Activity:
                   2020-03-09:
-------------------------------------------------
"""

from . import app
from .request_pacs import request_to_pacs
from .db_op import get_pacs_assem_by_id, get_assem_info_by_order_assem_id, save_pacs_assem_log
from .param_config import CurPosParams
from .err import SkipDelFlagException, NotFoundException
from .utils import get_init_dict
from datetime import datetime
from .models import DockingPacsAssemLog
import logging

log = logging.getLogger(__name__)


def _save_assem_log(order_id, username, sex, age, assem_id, assem_name, req_no, req_msg, req_status):
    assemLog = DockingPacsAssemLog()
    assemLog.ORDER_ID = order_id
    assemLog.USERNAME = username
    assemLog.SEX = sex
    assemLog.AGE = age
    assemLog.ASSEM_ID = assem_id
    assemLog.ASSEM_NAME = assem_name
    assemLog.REQ_NO = req_no
    assemLog.REQ_MSG = req_msg
    assemLog.REQ_STATUS = req_status
    assemLog.REQ_TIME = datetime.now()
    save_pacs_assem_log(assemLog)


def to_pacs():
    log.info('开始从配置文件中获取ID信息...')
    cur = CurPosParams('to_pacs')
    id = cur.get()
    log.info('获取到当前的ID：{}'.format(id))
    assem_changed = None

    req_status = '0'
    req_msg = ''
    pacs_dict = get_init_dict()
    try:
        assem_changed = get_pacs_assem_by_id(id, app.config['PLAT_DEPARMENT_IDS'])
        if not assem_changed:
            log.info('没有在项目组变动表中，发现比ID:{}大的新记录，程序将退出....')
            return
        log.info('获取到预约号为:{} 体检状态为:{} 操作状态为:{} 的记录'.format(assem_changed.ORDER_ID, assem_changed.EXAM_STATUS,
                                                           assem_changed.ASSEM_STATUS))
        if assem_changed.ASSEM_STATUS == '删除':
            raise SkipDelFlagException('跳过有删除标记的记录')

        request_to_pacs(
            order_id=assem_changed.ORDER_ID,
            assem_id=assem_changed.ELEMENT_ASSEM_ID,
            YLJGDM=app.config['YLJGDM'],
            YLJGMM=app.config['YLJGMM'],
            SQJGDM=app.config['SQJGDM'],
            build_dict=pacs_dict
        )

        req_status = '1'
        req_msg = '发送成功'

        cur.save(assem_changed.ID)
        log.info('发送成功!')
    except (SkipDelFlagException, NotFoundException) as e:
        req_status = '0'
        req_msg = repr(e)
        log.error('发送时发生错误')
        log.error(e)
        cur.save(assem_changed.ID)

    except Exception as e:
        req_status = '0'
        req_msg = repr(e)
        log.error('发送时发生错误')
        log.error(e)
    finally:
        if assem_changed:
            _save_assem_log(
                order_id=assem_changed.ORDER_ID,
                username=pacs_dict['PARAMS'].get('BRXM'),
                sex=pacs_dict['PARAMS'].get('BRXB'),
                age=pacs_dict['PARAMS'].get('BRNL'),
                assem_id=assem_changed.ELEMENT_ASSEM_ID,
                assem_name=assem_changed.NAME,
                req_no=pacs_dict['PARAMS'].get('SQDH'),
                req_status=req_status,
                req_msg=req_msg

            )
