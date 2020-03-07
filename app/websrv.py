# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     websrv_pacs
   Description :
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""

from spyne import ServiceBase
from spyne import Unicode
from spyne import rpc
from .err import InvalidParamException
import logging
from .utils import make_response, check_params
from .db_op import insert_lis_following, \
    insert_lis_dict, \
    insert_lis_wjz_following, \
    insert_pacs_following, \
    insert_pacs_dict, \
    insert_pacs_wjz_following

log = logging.getLogger(__name__)


class WebService(ServiceBase):
    """
    对外实现WebSerice服务
    """

    @rpc(Unicode, _returns=Unicode)
    def jyztUpload(self, params):
        """
        检验状态回传接口
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jyztUpload', params))
        try:
            param = check_params(params, 'PARAMS')
            log.info('开始进行入库操作...')
            insert_lis_following(param['PARAMS'])
            return make_response('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误，'.format('jyztUpload'))
            log.error(e)
            return make_response(None, e)

    @rpc(Unicode, _returns=Unicode)
    def jyxmDictionary(self, params):
        """
        检验中心推送检查项目字典表给his
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jyxmDictionary', params))
        try:
            param = check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('FORMLISTS', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/FORMLISTS'))
            insert_lis_dict(param['PARAMS'])
            return make_response('回传成功')

        except Exception as e:
            log.error('方法[{}]产生错误'.format('jyxmDictionary'))
            log.error(e)
            return make_response(None, e)

    @rpc(Unicode, _returns=Unicode)
    def lisWjz(self, params):
        """
        检验危急值
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('lisWjz', params))
        try:
            param = check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('ItemResultList', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/ItemResultList'))

            insert_lis_wjz_following(param['PARAMS'])
            return make_response('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误'.format('lisWjz'))
            log.error(e)
            return make_response(None, e)

    @rpc(Unicode, _returns=Unicode)
    def jcztUpload(self, params):
        """
        检查状态回传接口
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jcztUpload', params))
        try:
            param = check_params(params, 'PARAMS')
            log.info('开始进行入库操作...')
            insert_pacs_following(param['PARAMS'])
            return make_response('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误，'.format('jcztUpload'))
            log.error(e)
            return make_response(None, e)

    @rpc(Unicode, _returns=Unicode)
    def jcxmDictionary(self, params):
        """
        影像中心推送检查项目字典表给his。
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jcxmDictionary', params))
        try:
            param = check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('FORMLISTS', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/FORMLISTS'))
            insert_pacs_dict(param['PARAMS'])
            return make_response('回传成功')

        except Exception as e:
            log.error('方法[{}]产生错误'.format('jcxmDictionary'))
            log.error(e)
            return make_response(None, e)

    @rpc(Unicode, _returns=Unicode)
    def pacsWjz(self, params):
        """
        影像机构主动推送危急值给his
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('pacsWjz', params))
        try:
            param = check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('FORMLISTS', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/FORMLISTS'))

            insert_pacs_wjz_following(param['PARAMS'])
            return make_response('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误'.format('pacsWjz'))
            log.error(e)
            return make_response(None, e)
