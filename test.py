# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wdh
   date：          2020-03-03
-------------------------------------------------
   Change Activity:
                   2020-03-03:
-------------------------------------------------
"""

import logging
from logconf import load_my_logging_cfg
from app import redis
import datetime

log = logging.getLogger(__name__)
load_my_logging_cfg('test')

if __name__ == '__main__':
    log.info('测试日志')
    # log.info(redis_store.set('ho'))
    # redis.getset('wdh.ho', 'token', ex=20)
    # redis.expireat('wdh.ho','2020-03-03 18:33:00');
    # redis.set('wdh.ho', 'token')
    # redis.expireat('wdh.ho', datetime.datetime.now() + datetime.timedelta(seconds=30))
    # redis.pexpireat()

    # log.info(datetime.datetime.now().timetuple())

    # now = datetime.datetime(year=2020, month=3, day=3)
    # log.info((now.time().max - now.time()).seconds)

    # log.info(now.time().max.hour - now.time().second)
    # max = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # max = datetime.datetime.combine(now.today(), now.time().max)

    # log.info(max)
    #
    # log.info((max - now).seconds)

    # redis.expireat()

    # print(d)

    # ex = (max - now).seconds
    #
    # mex = (max - now).seconds
    #
    # log.info('ex={}'.format(mex))
    #
    # redis.set('wdh.ho', 'hello world', ex=ex)

    # log.info(redis.get('wdh.ho'))

    from app.websrv import _check_params

    params = """

        <PARAMS> 
          <FORMLISTS> 
            <FORMLIST> 
              <YLJGDM>310112001</YLJGDM>  
              <SQDH>2323</SQDH>  
              <BRID>111</BRID>  
              <BRXM>张三</BRXM>  
              <BRXB>1</BRXB>  
              <BRNL>22</BRNL>  
              <LXDH>132111111</LXDH>  
              <JTDZ>虹桥路1001号</JTDZ>  
              <YWLSH>321231</YWLSH>  
              <MZBZ>1</MZBZ>  
              <YXHM>0010</YXHM>  
              <JCXM>1212</JCXM>  
              <JCSJ>2018-11-11 10:10:10</JCSJ>  
              <JCLX>01</JCLX>  
              <XMDM>11</XMDM>  
              <JCBW>心脏</JCBW>  
              <BWBM/>  
              <JCMC>电脑多导联心电图</JCMC>  
              <YYBZ>1</YYBZ>  
              <YXBX>窦性心律；ST-T改变；</YXBX>  
              <JCTS>窦性心律；ST-T改变；</JCTS>  
              <JYBZ>窦性心律；ST-T改变；</JYBZ>  
              <WJZBZ>1</WJZBZ>  
              <SBM>SBM001</SBM>  
              <BZ>紧急问题，请处理！</BZ> 
            </FORMLIST>  
            <FORMLIST> 
              <YLJGDM>310112001</YLJGDM>  
              <SQDH>2323</SQDH>  
              <BRID>111</BRID>  
              <BRXM>张三</BRXM>  
              <BRXB>1</BRXB>  
              <BRNL>22</BRNL>  
              <LXDH>132111111</LXDH>  
              <JTDZ>虹桥路1001号</JTDZ>  
              <YWLSH>321231</YWLSH>  
              <MZBZ>1</MZBZ>  
              <YXHM>0010</YXHM>  
              <JCXM>1212</JCXM>  
              <JCSJ>2018-11-11 10:10:10</JCSJ>  
              <JCLX>01</JCLX>  
              <XMDM>11</XMDM>  
              <JCBW>心脏</JCBW>  
              <BWBM/>  
              <JCMC>电脑多导联心电图</JCMC>  
              <YYBZ>1</YYBZ>  
              <YXBX>窦性心律；ST-T改变；</YXBX>  
              <JCTS>窦性心律；ST-T改变；</JCTS>  
              <JYBZ>窦性心律；ST-T改变；</JYBZ>  
              <WJZBZ>1</WJZBZ>  
              <SBM>SBM002</SBM>  
              <BZ>紧急问题，请处理！</BZ> 
            </FORMLIST> 
          </FORMLISTS>  
          <SQJGDM>110112001</SQJGDM>  
          <TOKEN>12iui2912k</TOKEN> 
        </PARAMS>

    """
    # d = _check_params(params, 'PARAMS')
    # print(d.get('PARAMS').get('YLJGDM'))
    from app.websrv import WebService

    web = WebService()
    r = web.pacsWjz(params)
    log.info(r)
