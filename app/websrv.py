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
import xmltodict
from .err import InvalidParamException
import logging
from .db_op import insert_lis_following, \
    insert_lis_dict, \
    insert_lis_wjz_following, \
    insert_pacs_following, \
    insert_pacs_dict, \
    insert_pacs_wjz_following

log = logging.getLogger(__name__)


def _return(msg, ex=None):
    r = {
        'RETURN': {
            'FHZTM': None,
            'FHXX': None
        }}
    if ex:
        r['RETURN']['FHXX'] = repr(ex)
        if hasattr(ex, 'errcode'):
            r['RETURN']['FHZTM'] = ex.errcode
        else:
            r['RETURN']['FHZTM'] = 500
    else:
        r['RETURN']['FHXX'] = msg
        r['RETURN']['FHZTM'] = 200
    return xmltodict.unparse(r, full_document=True, pretty=True)


def _check_params(params, must_exist):
    """
    检查参数的前效性，并将xml格式的参数转为字典类型返回
    :param params:
    :return:
    """
    param = xmltodict.parse(params)
    if not param.get(must_exist, None):
        raise InvalidParamException('获取到的参数无效，在获取到的XML中没有找到必须节点[{}]'.format(must_exist))
    return param


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
            param = _check_params(params, 'PARAMS')
            log.info('开始进行入库操作...')
            insert_lis_following(param['PARAMS'])
            return _return('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误，'.format('jyztUpload'))
            log.error(e)
            return _return(None, e)

    @rpc(Unicode, _returns=Unicode)
    def jyxmDictionary(self, params):
        """
        检验中心推送检查项目字典表给his
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jyxmDictionary', params))
        try:
            param = _check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('FORMLISTS', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/FORMLISTS'))
            insert_lis_dict(param['PARAMS'])
            return _return('回传成功')

        except Exception as e:
            log.error('方法[{}]产生错误'.format('jyxmDictionary'))
            log.error(e)
            return _return(None, e)

    @rpc(Unicode, _returns=Unicode)
    def lisWjz(self, params):
        """
        检验危急值
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('lisWjz', params))
        try:
            param = _check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('ItemResultList', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/ItemResultList'))

            insert_lis_wjz_following(param['PARAMS'])
            return _return('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误'.format('lisWjz'))
            log.error(e)
            return _return(None, e)

    @rpc(Unicode, _returns=Unicode)
    def jcztUpload(self, params):
        """
        检查状态回传接口
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jcztUpload', params))
        try:
            param = _check_params(params, 'PARAMS')
            log.info('开始进行入库操作...')
            insert_pacs_following(param['PARAMS'])
            return _return('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误，'.format('jcztUpload'))
            log.error(e)
            return _return(None, e)

    @rpc(Unicode, _returns=Unicode)
    def jcxmDictionary(self, params):
        """
        影像中心推送检查项目字典表给his。
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('jcxmDictionary', params))
        try:
            param = _check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('FORMLISTS', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/FORMLISTS'))
            insert_pacs_dict(param['PARAMS'])
            return _return('回传成功')

        except Exception as e:
            log.error('方法[{}]产生错误'.format('jcxmDictionary'))
            log.error(e)
            return _return(None, e)

    @rpc(Unicode, _returns=Unicode)
    def pacsWjz(self, params):
        """
        影像机构主动推送危急值给his
        :param params:
        :return:
        """
        log.info('方法:[{}]  获取到参数:[{}]'.format('pacsWjz', params))
        try:
            param = _check_params(params, 'PARAMS')
            log.info('开始检查参数数据结构的有效性')
            if not param['PARAMS'].get('FORMLISTS', None):
                raise InvalidParamException('获取到的参数无效,缺少节点[{}]'.format('PARAMS/FORMLISTS'))

            insert_pacs_wjz_following(param['PARAMS'])
            return _return('回传成功')
        except Exception as e:
            log.error('方法[{}]产生错误'.format('pacsWjz'))
            log.error(e)
            return _return(None, e)
