# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task_to_lis
   Description :   向lis发数据的定时任务
   Author :       wdh
   date：          2020-03-08
-------------------------------------------------
   Change Activity:
                   2020-03-08:
-------------------------------------------------
"""

from . import app
from .request_lis import request_to_lis
from .db_op import get_barcode_changed, save_barcode_changed
from .param_config import CurPosParams
from .err import SkipDelFlagException, NotFoundException
from .utils import get_init_dict
from datetime import datetime
import logging

log = logging.getLogger(__name__)


def to_lis():
    log.info('开始从配置文件中获取ID信息...')
    cur = CurPosParams('to_lis')
    id = cur.get()
    log.info('获取到当前的ID：{}'.format(id))
    barcode_changed = None
    try:
        barcode_changed = get_barcode_changed(id)
        if not barcode_changed:
            log.info('没有在条码变动表中，发现比ID:{}大的新条码，程序将退出....'.format(id))
            return
        log.info('获取到条码号为:{}  操作状态为:{} 的记录'.format(barcode_changed.BARCODE_ID, barcode_changed.OP_TYPE))
        if barcode_changed.OP_TYPE == '删除':
            raise SkipDelFlagException('跳过有删除标记的记录')

        lis_dict = get_init_dict()

        request_to_lis(barcode=barcode_changed.BARCODE_ID,
                       YLJGDM=app.config['YLJGDM'],
                       YLJGMM=app.config['YLJGMM'],
                       SYSDM=app.config['SYSDM'],
                       SQJGDM=app.config['SQJGDM'],
                       build_dict=lis_dict
                       )
        barcode_changed.REQ_NO = lis_dict['PARAMS']['SQDH']
        barcode_changed.REQ_STATUS = '1'
        barcode_changed.REQ_MSG = '发送成功'
        cur.save(barcode_changed.ID)
        log.info('发送成功!')
    except (SkipDelFlagException, NotFoundException) as e:
        barcode_changed.REQ_STATUS = '0'
        barcode_changed.REQ_MSG = repr(e)
        cur.save(barcode_changed.ID)
        log.error('发送时发生错误')
        log.error(e)

    except Exception as e:
        barcode_changed.REQ_STATUS = '0'
        barcode_changed.REQ_MSG = repr(e)
        log.error('发送时发生错误')
        log.error(e)
    finally:
        if barcode_changed:
            barcode_changed.REQ_TIME = datetime.now()
            save_barcode_changed(barcode_changed)
