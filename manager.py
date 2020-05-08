# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     manager
   Description :
   Author :       wdh
   date：          2020-03-08
-------------------------------------------------
   Change Activity:
                   2020-03-08:
-------------------------------------------------
"""

import logging
from logconf import load_my_logging_cfg
from apscheduler.schedulers.blocking import BlockingScheduler
from app import app
from flask_script import Manager, Command
from app.task_to_lis import to_lis
from app.task_to_pacs import to_pacs
from app.task_lis_to_phexam import lis_phexam
from app.task_pacs_to_phexam import pacs_phexam

log = logging.getLogger(__name__)

manager = Manager(app)


def _get_scheduler():
    return BlockingScheduler(
        executors=app.config['SCHEDULER_EXECUTORS'],
        job_defaults=app.config['SCHEDULER_JOB_DEFAULTS'])


def _begin_scheduler(scheduler):
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info('任务结束.')
        scheduler.shutdown()


class ToLis(Command):
    """
    向lis定时转输
    """

    def run(self):
        load_my_logging_cfg('to_lis')
        # # 第10秒一次
        scheduler = _get_scheduler()
        scheduler.add_job(to_lis, id='trans_to_lis', trigger='cron', second='*/10', replace_existing=True)
        _begin_scheduler(scheduler)


class ToPacs(Command):
    """
      向PACS定时转输
    """

    def run(self):
        load_my_logging_cfg('to_pacs')
        # # 第10秒一次
        scheduler = _get_scheduler()
        scheduler.add_job(to_pacs, id='trans_to_pacs', trigger='cron', second='*/10', replace_existing=True)
        _begin_scheduler(scheduler)


class LisToPhexam(Command):
    """
      接收LIS结果数据
    """

    def run(self):
        load_my_logging_cfg('lis_to_phexam')
        # # 第10秒一次
        scheduler = _get_scheduler()
        scheduler.add_job(lis_phexam, id='lis_to_phexam', trigger='cron', second='*/10', replace_existing=True)
        _begin_scheduler(scheduler)


class PacsToPhexam(Command):
    """
     接收PACS结果数据
    """

    def run(self):
        load_my_logging_cfg('pacs_to_phexam')
        # # 第10秒一次
        scheduler = _get_scheduler()
        scheduler.add_job(pacs_phexam, id='pacs_to_phexam', trigger='cron', second='*/10', replace_existing=True)
        _begin_scheduler(scheduler)


manager.add_command('to_lis', ToLis())
manager.add_command('to_pacs', ToPacs())
manager.add_command('lis_to_phexam', LisToPhexam())
manager.add_command('pacs_to_phexam', PacsToPhexam())

if __name__ == '__main__':
    manager.run()
