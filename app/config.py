# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""

# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       wdh
   date：          2019/4/12
-------------------------------------------------
   Change Activity:
                   2019/4/12:
-------------------------------------------------
"""

import os

_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# 参数配置文件
_confdir = os.path.join(_basedir, 'conf')
if not os.path.exists(_confdir):
    os.mkdir(_confdir)

# 临时目录文件夹
_tempdir = os.path.join(_basedir, 'temp')
if not os.path.exists(_tempdir):
    os.mkdir(_tempdir)


class Config:
    JSON_AS_ASCII = False

    # 配置文件路径
    CONF_PATH = _confdir

    # 临时文件夹路径
    TEMP_PATH = _tempdir

    MEDIA_SERVER_URL = 'http://lanshankeji.vicp.net:9099/mediasrv/'

    SERVER_URL = 'http://lanshankeji.vicp.net:9099/'

    # 蓝滴体检数据库
    JK_USERNAME_CONST = 'third'
    JK_PASSWORD_CONST = '1234'

    JK_HOST_CONST = 'lanshankeji.vicp.net'
    JK_DATABASE_CONST = 'jk_lf_plus'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        JK_USERNAME_CONST, JK_PASSWORD_CONST, JK_HOST_CONST, JK_DATABASE_CONST)

    # SQLALCHEMY_DATABASE_URI = 'oracle://%s:%s@%s/%s' % (
    #     JK_USERNAME_CONST, JK_PASSWORD_CONST, JK_HOST_CONST, JK_DATABASE_CONST)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 蓝滴体检系统登录用户、密码
    JK_EXAM_USERNAME = 'system'
    JK_EXAM_PASSWORD = '1234'

    # Redis配置
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    # from apscheduler.jobstores.redis import RedisJobStore

    # Redis配置
    # SCHEDULER_JOBSTORES = {
    #    'default': RedisJobStore(host=REDIS_HOST, port=REDIS_PORT)
    # }

    # 配置定时任务
    SCHEDULER_EXECUTORS = {
        'default': {
            'type': 'threadpool',
            'max_workers': 1
        },

    }
    #
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 600
    }

    # 邮件相关
    MAIL_MESSAGE = {
        'host': 'smtp.livingjz.com',
        'username': 'donghai.wu@livingjz.com',
        'password': 'Killme123456',
        'sender': 'donghai.wu@livingjz.com',
        'receivers': ['459834034@qq.com', ],
        'from': '国瑞怡康体检系统'
    }

    SCHEDULER_API_ENABLED = True

    # 失败时，是否发送邮件
    IS_SEND_MAIL = False

    # 本医疗机构代码
    YLJGDM = '310112001'

    # 本医疗机构密码
    YLJGMM = '310112001'

    # 申请医疗机构代码
    SQJGDM = '310112001'

    # 实验证代码
    SYSDM = '310112001'

    # 平台LIS接口URL
    PLAT_LIS_URL = 'http://55.0.0.1:9090/bsoftHQPlatform/hisToLisWs?wsdl'

    # 平台PACS接口URL
    PLAT_PACS_URL = 'http://55.0.0.1:9090/bsoftHQPlatform/hisToPacsWs?wsdl'

    # 平台安全接口URL
    PLAT_SECURITY_URL = 'http://55.0.0.1:9090/bsoftHQPlatform/securitykeys?wsdl'

    # 要上传到平台的PACS类科室ID列表
    PLAT_DEPARMENT_IDS = [5, 6, 20, 21]

#
# # 每天的19点至23点，0点到6点,每分种
# JOBS = [
#     {
#         'id': 'job_trans_to_yibao',
#         'func': 'yibao.task:trans',
#         'args': None,
#         'replace_existing': True,
#         'trigger': {
#             'type': 'cron',
#             'day': '*',
#             # 'hour': '19-23,0-6',
#             'hour': '17-23',
#             'second': '0,10,20,30,40,50'
#             # 'minute': '*/1'
#         }
#     }
#
# ]
#
# SCHEDULER_API_ENABLED = True
# TRAP_BAD_REQUEST_ERRORS = True
