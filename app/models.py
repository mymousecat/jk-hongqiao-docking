# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2020-03-04
-------------------------------------------------
   Change Activity:
                   2020-03-04:
-------------------------------------------------
"""

from . import db


class DockingLisFollowing(db.Model):
    """
      LIS状态回传表
    """
    __tablename__ = 't_docking_lis_following'
    id = db.Column(db.Integer, primary_key=True)
    YLJGDM = db.Column(db.String)
    SQJGDM = db.Column(db.String)
    SYSDM = db.Column(db.String)
    BRID = db.Column(db.String)
    SQDH = db.Column(db.String)
    YWLSH = db.Column(db.String)
    MZBZ = db.Column(db.String)
    SJTM = db.Column(db.String)
    ZXTM = db.Column(db.String)
    BRXM = db.Column(db.String)
    BRXB = db.Column(db.String)
    BRNL = db.Column(db.String)
    SJRQ = db.Column(db.String)
    JYLXBM = db.Column(db.String)
    BGDMC = db.Column(db.String)
    ZTBZ = db.Column(db.String)
    TOKEN = db.Column(db.String)


class DockingPacsFollowing(db.Model):
    """
      PACS状态回传表
    """
    __tablename__ = 't_docking_pacs_following'
    id = db.Column(db.Integer, primary_key=True)
    YLJGDM = db.Column(db.String)
    SQJGDM = db.Column(db.String)
    BRID = db.Column(db.String)
    SQDH = db.Column(db.String)
    YWLSH = db.Column(db.String)
    MZBZ = db.Column(db.String)
    JCXM = db.Column(db.String)
    BRXM = db.Column(db.String)
    BRXB = db.Column(db.String)
    BRNL = db.Column(db.String)
    JCSJ = db.Column(db.String)
    JCMC = db.Column(db.String)
    ZTBZ = db.Column(db.String)
    TPDQDZ = db.Column(db.String)
    TWBGWJLLDZ = db.Column(db.String)
    TOKEN = db.Column(db.String)


class DockingLisDict(db.Model):
    """
      检验项目字典表
    """
    __tablename__ = 't_docking_lis_dict'
    id = db.Column(db.Integer, primary_key=True)
    YLJGDM = db.Column(db.String)
    SYSDM = db.Column(db.String)
    YBMLBM = db.Column(db.String)
    XMWSDM = db.Column(db.String)
    XMMC = db.Column(db.String)
    XMBM = db.Column(db.String)
    SFDW = db.Column(db.String)
    SFDJ = db.Column(db.String)
    SFXDLB = db.Column(db.String)
    SYBZ = db.Column(db.String)
    YNZJBZ = db.Column(db.String)
    TBSM = db.Column(db.String)
    BZSM = db.Column(db.String)
    SQJGDM = db.Column(db.String)
    XGBZ = db.Column(db.String)
    TOKEN = db.Column(db.String)


class DockingPacsDict(db.Model):
    """
      检查类项目字典表
    """
    __tablename__ = 't_docking_pacs_dict'
    id = db.Column(db.Integer, primary_key=True)
    YLJGDM = db.Column(db.String)
    YYZBDM = db.Column(db.String)
    YBMLBM = db.Column(db.String)
    XMWSDM = db.Column(db.String)
    JCLX = db.Column(db.String)
    XMMC = db.Column(db.String)
    XMBM = db.Column(db.String)
    JCBW = db.Column(db.String)
    BWBM = db.Column(db.String)
    SFDW = db.Column(db.String)
    SFDJ = db.Column(db.String)
    SFXDLB = db.Column(db.String)
    SYBZ = db.Column(db.String)
    YNZJBZ = db.Column(db.String)
    TBSM = db.Column(db.String)
    BZSM = db.Column(db.String)
    SQJGDM = db.Column(db.String)
    XGBZ = db.Column(db.String)
    TOKEN = db.Column(db.String)


class DockingLisWjzFollowing(db.Model):
    """
      LIS危急值结果流水表
    """
    __tablename__ = 't_docking_lis_wjz_following'
    id = db.Column(db.Integer, primary_key=True)
    YLJGDM = db.Column(db.String)
    SQJGDM = db.Column(db.String)
    SYSDM = db.Column(db.String)
    SQDH = db.Column(db.String)
    BRID = db.Column(db.String)
    BRXM = db.Column(db.String)
    BRXB = db.Column(db.String)
    BRNL = db.Column(db.String)
    LXDH = db.Column(db.String)
    JTDZ = db.Column(db.String)
    YWLSH = db.Column(db.String)
    MZBZ = db.Column(db.String)
    BBLX = db.Column(db.String)
    JYTM = db.Column(db.String)
    SFXMDM = db.Column(db.String)
    SFXMMC = db.Column(db.String)
    XH = db.Column(db.String)
    XMDM = db.Column(db.String)
    XMMC = db.Column(db.String)
    JCJG = db.Column(db.String)
    JLDW = db.Column(db.String)
    CKFW = db.Column(db.String)
    YCTS = db.Column(db.String)
    WJZBZ = db.Column(db.String)
    SBM = db.Column(db.String)
    BZ = db.Column(db.String)
    TOKEN = db.Column(db.String)


class DockingPacsWjzFollowing(db.Model):
    """
      影像危急值（审核中）
    """
    __tablename__ = 't_docking_pacs_wjz_following'
    id = db.Column(db.Integer, primary_key=True)
    YLJGDM = db.Column(db.String)
    SQJGDM = db.Column(db.String)
    SQDH = db.Column(db.String)
    BRID = db.Column(db.String)
    BRXM = db.Column(db.String)
    BRXB = db.Column(db.String)
    BRNL = db.Column(db.String)
    LXDH = db.Column(db.String)
    JTDZ = db.Column(db.String)
    YWLSH = db.Column(db.String)
    MZBZ = db.Column(db.String)
    YXHM = db.Column(db.String)
    JCXM = db.Column(db.String)
    JCSJ = db.Column(db.String)
    JCLX = db.Column(db.String)
    XMDM = db.Column(db.String)
    JCBW = db.Column(db.String)
    BWBM = db.Column(db.String)
    JCMC = db.Column(db.String)
    YYBZ = db.Column(db.String)
    YXBX = db.Column(db.String)
    JCTS = db.Column(db.String)
    JYBZ = db.Column(db.String)
    WJZBZ = db.Column(db.String)
    SBM = db.Column(db.String)
    BZ = db.Column(db.String)
    TOKEN = db.Column(db.String)