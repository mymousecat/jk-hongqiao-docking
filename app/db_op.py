# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""

from . import db
from .models import DockingLisDict, DockingLisFollowing, DockingPacsWjzFollowing, DockingPacsDict, DockingPacsFollowing, \
    DockingLisWjzFollowing


def insert_lis_dict(lis_dict):
    """
    插入或修改LIS字典
    :param lis_dict:
    :return:
    """
    try:
        formlists = lis_dict['FORMLISTS']

        forms = formlists['FORMLIST']

        ll = None
        if isinstance(forms, list):
            ll = forms
        else:
            ll = [forms]

        for form in ll:

            xmbm = form.get('XMBM', None)
            lisDict = db.session.query(DockingLisDict).filter(DockingLisDict.XMBM == xmbm).first()
            if lisDict is None:
                lisDict = DockingLisDict()

            lisDict.YLJGDM = lis_dict.get('YLJGDM', None)
            lisDict.SYSDM = lis_dict.get('SYSDM', None)
            lisDict.TOKEN = lis_dict.get('TOKEN', None)
            lisDict.SQJGDM = lis_dict.get('SQJGDM', None)

            lisDict.YBMLBM = form.get('YBMLBM', None)
            lisDict.XMWSDM = form.get('XMWSDM', None)
            lisDict.XMMC = form.get('XMMC', None)
            lisDict.XMBM = form.get('XMBM', None)
            lisDict.SFDW = form.get('SFDW', None)
            lisDict.SFDJ = form.get('SFDJ', None)
            lisDict.SFXDLB = form.get('SFXDLB', None)
            lisDict.SYBZ = form.get('SYBZ', None)
            lisDict.YNZJBZ = form.get('YNZJBZ', None)
            lisDict.TBSM = form.get('TBSM', None)
            lisDict.BZSM = form.get('BZSM', None)
            lisDict.XGBZ = form.get('XGBZ', None)

            if lisDict.id is None:
                db.session.add(lisDict)
            else:
                db.session.merge(lisDict)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def insert_lis_following(lis_following_dict):
    """
    插入LIS状态流水表
    :param lis_following_dict:
    :return:
    """
    try:
        lisFollowing = DockingLisFollowing()
        lisFollowing.YLJGDM = lis_following_dict.get('YLJGDM', None)
        lisFollowing.SQJGDM = lis_following_dict.get('SQJGDM', None)
        lisFollowing.SYSDM = lis_following_dict.get('SYSDM', None)
        lisFollowing.BRID = lis_following_dict.get('BRID', None)
        lisFollowing.SQDH = lis_following_dict.get('SQDH', None)
        lisFollowing.YWLSH = lis_following_dict.get('YWLSH', None)
        lisFollowing.MZBZ = lis_following_dict.get('MZBZ', None)
        lisFollowing.SJTM = lis_following_dict.get('SJTM', None)
        lisFollowing.ZXTM = lis_following_dict.get('ZXTM', None)
        lisFollowing.BRXM = lis_following_dict.get('BRXM', None)
        lisFollowing.BRXB = lis_following_dict.get('BRXB', None)
        lisFollowing.BRNL = lis_following_dict.get('BRNL', None)
        lisFollowing.SJRQ = lis_following_dict.get('SJRQ', None)
        lisFollowing.JYLXBM = lis_following_dict.get('JYLXBM', None)
        lisFollowing.BGDMC = lis_following_dict.get('BGDMC', None)
        lisFollowing.ZTBZ = lis_following_dict.get('ZTBZ', None)
        lisFollowing.TOKEN = lis_following_dict.get('TOKEN', None)
        db.session.add(lisFollowing)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


# DockingLisWjzFollowing
def insert_lis_wjz_following(lis_wjz_following_dict):
    """
    插入LIS危机值流水表
    :param lis_wjz_following_dict:
    :return:
    """
    try:
        itemResultList = lis_wjz_following_dict['ItemResultList']
        itemResults = itemResultList['ItemResult']
        ll = None
        if isinstance(itemResults, list):
            ll = itemResults
        else:
            ll = [itemResults]

        for itemResult in ll:
            lisWjzFollowing = DockingLisWjzFollowing()
            lisWjzFollowing.YLJGDM = lis_wjz_following_dict.get('YLJGDM', None)
            lisWjzFollowing.SQJGDM = lis_wjz_following_dict.get('SQJGDM', None)
            lisWjzFollowing.SYSDM = lis_wjz_following_dict.get('SYSDM', None)
            lisWjzFollowing.SQDH = lis_wjz_following_dict.get('SQDH', None)
            lisWjzFollowing.BRID = lis_wjz_following_dict.get('BRID', None)
            lisWjzFollowing.BRXM = lis_wjz_following_dict.get('BRXM', None)
            lisWjzFollowing.BRXB = lis_wjz_following_dict.get('BRXB', None)
            lisWjzFollowing.BRNL = lis_wjz_following_dict.get('BRNL', None)
            lisWjzFollowing.LXDH = lis_wjz_following_dict.get('LXDH', None)
            lisWjzFollowing.JTDZ = lis_wjz_following_dict.get('JTDZ', None)
            lisWjzFollowing.YWLSH = lis_wjz_following_dict.get('YWLSH', None)
            lisWjzFollowing.MZBZ = lis_wjz_following_dict.get('MZBZ', None)
            lisWjzFollowing.BBLX = lis_wjz_following_dict.get('BBLX', None)
            lisWjzFollowing.JYTM = lis_wjz_following_dict.get('JYTM', None)
            lisWjzFollowing.SFXMDM = lis_wjz_following_dict.get('SFXMDM', None)
            lisWjzFollowing.SFXMMC = lis_wjz_following_dict.get('SFXMMC', None)
            lisWjzFollowing.TOKEN = lis_wjz_following_dict.get('TOKEN', None)

            lisWjzFollowing.XH = itemResult.get('XH', None)
            lisWjzFollowing.XMDM = itemResult.get('XMDM', None)
            lisWjzFollowing.XMMC = itemResult.get('XMMC', None)
            lisWjzFollowing.JCJG = itemResult.get('JCJG', None)
            lisWjzFollowing.JLDW = itemResult.get('JLDW', None)
            lisWjzFollowing.CKFW = itemResult.get('CKFW', None)
            lisWjzFollowing.YCTS = itemResult.get('YCTS', None)
            lisWjzFollowing.WJZBZ = itemResult.get('WJZBZ', None)
            lisWjzFollowing.SBM = itemResult.get('SBM', None)
            lisWjzFollowing.BZ = itemResult.get('BZ', None)

            db.session.add(lisWjzFollowing)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


# DockingPacsDict
def insert_pacs_dict(pacs_dict):
    """
    检查类项目字曲表
    :param pacs_dict:
    :return:
    """
    try:
        formlists = pacs_dict['FORMLISTS']
        forms = formlists['FORMLIST']
        ll = None
        if isinstance(forms, list):
            ll = forms
        else:
            ll = [forms]

        for form in ll:
            pacsDict = DockingPacsDict()
            pacsDict.YLJGDM = pacs_dict.get('YLJGDM', None)
            pacsDict.SQJGDM = pacs_dict.get('SQJGDM', None)
            pacsDict.TOKEN = pacs_dict.get('TOKEN', None)

            pacsDict.YYZBDM = form.get('YYZBDM', None)
            pacsDict.YBMLBM = form.get('YBMLBM', None)
            pacsDict.XMWSDM = form.get('XMWSDM', None)
            pacsDict.JCLX = form.get('JCLX', None)
            pacsDict.XMMC = form.get('XMMC', None)
            pacsDict.XMBM = form.get('XMBM', None)
            pacsDict.JCBW = form.get('JCBW', None)
            pacsDict.BWBM = form.get('BWBM', None)
            pacsDict.SFDW = form.get('SFDW', None)
            pacsDict.SFDJ = form.get('SFDJ', None)
            pacsDict.SFXDLB = form.get('SFXDLB', None)
            pacsDict.SYBZ = form.get('SYBZ', None)
            pacsDict.YNZJBZ = form.get('YNZJBZ', None)
            pacsDict.TBSM = form.get('TBSM', None)
            pacsDict.BZSM = form.get('BZSM', None)
            pacsDict.XGBZ = form.get('XGBZ', None)
            db.session.add(pacsDict)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close


# DockingPacsFollowing
def insert_pacs_following(pacs_following_dict):
    """
    插入检查类状态流水表
    :param pacs_following_dict:
    :return:
    """
    try:
        pacsFollowing = DockingPacsFollowing()
        pacsFollowing.YLJGDM = pacs_following_dict.get('YLJGDM', None)
        pacsFollowing.SQJGDM = pacs_following_dict.get('SQJGDM', None)
        pacsFollowing.BRID = pacs_following_dict.get('BRID', None)
        pacsFollowing.SQDH = pacs_following_dict.get('SQDH', None)
        pacsFollowing.YWLSH = pacs_following_dict.get('YWLSH', None)
        pacsFollowing.MZBZ = pacs_following_dict.get('MZBZ', None)
        pacsFollowing.JCXM = pacs_following_dict.get('JCXM', None)
        pacsFollowing.BRXM = pacs_following_dict.get('BRXM', None)
        pacsFollowing.BRXB = pacs_following_dict.get('BRXB', None)
        pacsFollowing.BRNL = pacs_following_dict.get('BRNL', None)
        pacsFollowing.JCSJ = pacs_following_dict.get('JCSJ', None)
        pacsFollowing.JCMC = pacs_following_dict.get('JCMC', None)
        pacsFollowing.ZTBZ = pacs_following_dict.get('ZTBZ', None)
        pacsFollowing.TPDQDZ = pacs_following_dict.get('TPDQDZ', None)
        pacsFollowing.TWBGWJLLDZ = pacs_following_dict.get('TWBGWJLLDZ', None)
        pacsFollowing.TOKEN = pacs_following_dict.get('TOKEN', None)
        db.session.add(pacsFollowing)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


# DockingPacsWjzFollowing
def insert_pacs_wjz_following(pacs_wjz_following_dict):
    """
    检查类危急值
    :param pacs_wjz_following_dict:
    :return:
    """
    try:
        formlists = pacs_wjz_following_dict['FORMLISTS']
        forms = formlists['FORMLIST']
        ll = None
        if isinstance(forms, list):
            ll = forms
        else:
            ll = [forms]

        for form in ll:
            pacsWjzFollowing = DockingPacsWjzFollowing()
            pacsWjzFollowing.SQJGDM = pacs_wjz_following_dict.get('SQJGDM', None)
            pacsWjzFollowing.TOKEN = pacs_wjz_following_dict.get('TOKEN', None)

            pacsWjzFollowing.YLJGDM = form.get('YLJGDM', None)
            pacsWjzFollowing.SQDH = form.get('SQDH', None)
            pacsWjzFollowing.BRID = form.get('BRID', None)
            pacsWjzFollowing.BRXM = form.get('BRXM', None)
            pacsWjzFollowing.BRXB = form.get('BRXB', None)
            pacsWjzFollowing.BRNL = form.get('BRNL', None)
            pacsWjzFollowing.LXDH = form.get('LXDH', None)
            pacsWjzFollowing.JTDZ = form.get('JTDZ', None)
            pacsWjzFollowing.YWLSH = form.get('YWLSH', None)
            pacsWjzFollowing.MZBZ = form.get('MZBZ', None)
            pacsWjzFollowing.YXHM = form.get('YXHM', None)
            pacsWjzFollowing.JCXM = form.get('JCXM', None)
            pacsWjzFollowing.JCSJ = form.get('JCSJ', None)
            pacsWjzFollowing.JCLX = form.get('JCLX', None)
            pacsWjzFollowing.XMDM = form.get('XMDM', None)
            pacsWjzFollowing.JCBW = form.get('JCBW', None)
            pacsWjzFollowing.BWBM = form.get('BWBM', None)
            pacsWjzFollowing.JCMC = form.get('JCMC', None)
            pacsWjzFollowing.YYBZ = form.get('YYBZ', None)
            pacsWjzFollowing.YXBX = form.get('YXBX', None)
            pacsWjzFollowing.JCTS = form.get('JCTS', None)
            pacsWjzFollowing.JYBZ = form.get('JYBZ', None)
            pacsWjzFollowing.WJZBZ = form.get('WJZBZ', None)
            pacsWjzFollowing.SBM = form.get('SBM', None)
            pacsWjzFollowing.BZ = form.get('BZ', None)

            db.session.add(pacsWjzFollowing)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()
