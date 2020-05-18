# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task_nj_to_phexam
   Description :
   Author :       wdh
   date：          2020-05-18
-------------------------------------------------
   Change Activity:
                   2020-05-18:
-------------------------------------------------
"""

import logging
from .param_config import CurPosParams
from .db_op import get_next_tj_nj
from .nj_to_phexam import nj_to_exam
from . import appconfig
from .err import InvalidParamException
from jktj.tjexception import TJException

log = logging.getLogger(__name__)


def nj_phexam():
    log.info('开始从配置文件中获取ID信息...')
    cur = CurPosParams('nj_to_phexam')
    id = cur.get()
    log.info('获取到当前的ID：{}'.format(id))
    tjPacsResult = None
    try:
        tjPacsResult = get_next_tj_nj(id)
        if not tjPacsResult:
            log.info('没有在内镜结果表中，发现比ID:{}大的新结果，程序将退出....'.format(id))
            return
        log.info('获取到id:{}  预约号:{}  部位:{}'.format(tjPacsResult.id, tjPacsResult.register_num,
                                                  tjPacsResult.check_part))

        log.info('开始上传，，，')

        nj_to_exam(tjPacsResult, appconfig['NJ_DEPARTMENT_ID'])

        cur.save(tjPacsResult.id)

    except (InvalidParamException, TJException) as e:
        cur.save(tjPacsResult.id)
        log.error('接收内镜结果时发生错误,预约号为:{}  部位为:{}'.format(tjPacsResult.register_num, tjPacsResult.check_part))
        log.error(e)

    except Exception as e:
        log.error('接收内镜结果时发生错误,预约号为:{}  部位为:{}'.format(tjPacsResult.register_num, tjPacsResult.check_part))
        log.error(e)
