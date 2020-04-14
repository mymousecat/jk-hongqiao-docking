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


class DockingLisRequestView(db.Model):
    """
     通过样本号查询项目信息视图
    """
    __tablename__ = 'v_docking_lis_request_view'
    ID = db.Column(db.String, primary_key=True)
    BARCODE_ID = db.Column(db.String)
    ORDER_ID = db.Column(db.String)
    # ELEMENT_ASSEM_ID = db.Column(db.String)
    SPECIMEN_TYPE = db.Column(db.String)
    SPECIMEN_TYPE_NAME = db.Column(db.String)
    ASSEM_CODE = db.Column(db.String)
    ASSEM_NAME = db.Column(db.String)
    ELEMENT_CODE = db.Column(db.String)
    ELEMENT_NAME = db.Column(db.String)
    USERNAME = db.Column(db.String)
    SEX = db.Column(db.String)
    AGE = db.Column(db.Integer)
    INITIATOR = db.Column(db.String)
    INITIAL_TIME = db.Column(db.DateTime)
    BIRTHDAY = db.Column(db.Date)
    ADDRESS = db.Column(db.String)
    TELEPHONE = db.Column(db.String)
    CERT_TYPE = db.Column(db.String)
    CERT_ID = db.Column(db.String)
    ARRIVAL_DATE = db.Column(db.DateTime)
    DEPARMENT = db.Column(db.String)


# t_docking_barcode_changed
class DockingBarcodeChanged(db.Model):
    __tablename__ = 't_docking_barcode_changed'
    ID = db.Column(db.BigInteger, primary_key=True)
    ORDER_ID = db.Column(db.String)
    BARCODE_ID = db.Column(db.String)
    BARCODE_ASSEM_TYPE_ID = db.Column(db.String)
    ASSEM_SHORT_NAMES = db.Column(db.String)
    DELIVERY_SYMBOL = db.Column(db.String)
    INITIATOR = db.Column(db.String)
    INITIAL_TIME = db.Column(db.DateTime)
    OP_TYPE = db.Column(db.String)
    CHANGE_USER = db.Column(db.String)
    CHANGE_TIME = db.Column(db.DateTime)
    REQ_NO = db.Column(db.String)
    REQ_TIME = db.Column(db.String)
    REQ_STATUS = db.Column(db.String)
    REQ_MSG = db.Column(db.String)


# v_docking_assems_changed
class DockingAssemsChanged(db.Model):
    """
      项目变动通知流水表（视图),体检信息、收费都会变动
    """
    __tablename__ = 'v_docking_assems_changed'
    ID = db.Column(db.Integer, primary_key=True)
    ORDER_ID = db.Column(db.String)
    ELEMENT_ASSEM_ID = db.Column(db.String)
    UNIT_OR_OWN = db.Column(db.String)
    COST_STATUS = db.Column(db.String)
    EXAM_STATUS = db.Column(db.String)
    ASSEM_STATUS = db.Column(db.String)
    OP_ID = db.Column(db.String)
    DIFFPRICE_STATUS = db.Column(db.String)
    DIFFPRICE_COST_STATUS = db.Column(db.String)
    DEPARTMENT_ID = db.Column(db.String)
    NAME = db.Column(db.String)
    ASSEM_CODE = db.Column(db.String)


# v_docking_pacs_request_view
class DockingPacsRequestView(db.Model):
    """
      预约项目组表
    """
    __tablename__ = 'v_docking_pacs_request_view'
    ID = db.Column(db.String, primary_key=True)
    ORDER_ID = db.Column(db.String)
    ELEMENT_ASSEM_ID = db.Column(db.String)
    ASSEM_CODE = db.Column(db.String)
    ASSEM_NAME = db.Column(db.String)
    ELEMENT_CODE = db.Column(db.String)
    ELEMENT_NAME = db.Column(db.String)
    USERNAME = db.Column(db.String)
    SEX = db.Column(db.String)
    AGE = db.Column(db.Integer)
    INITIATOR = db.Column(db.String)
    INITIAL_TIME = db.Column(db.DateTime)
    BIRTHDAY = db.Column(db.Date)
    ADDRESS = db.Column(db.String)
    TELEPHONE = db.Column(db.String)
    CERT_TYPE = db.Column(db.String)
    CERT_ID = db.Column(db.String)
    ARRIVAL_DATE = db.Column(db.DateTime)
    DEPARMENT = db.Column(db.String)
    DEPARTMENT_ID = db.Column(db.Integer)


# t_docking_pacs_assem_log
class DockingPacsAssemLog(db.Model):
    """
     pacs数据平台上传日志表
    """
    __tablename__ = 't_docking_pacs_assem_log'
    ID = db.Column(db.Integer, primary_key=True)
    ORDER_ID = db.Column(db.String)
    USERNAME = db.Column(db.String)
    SEX = db.Column(db.String)
    AGE = db.Column(db.String)
    ASSEM_ID = db.Column(db.String)
    ASSEM_NAME = db.Column(db.String)
    REQ_NO = db.Column(db.String)
    REQ_TIME = db.Column(db.DateTime)
    REQ_STATUS = db.Column(db.String)
    REQ_MSG = db.Column(db.String)


class BarcodeDetail(db.Model):
    __tablename__ = 't_barcode_detail'
    ID = db.Column(db.Integer, primary_key=True)
    BARCODE_ID = db.Column(db.String)
    ELEMENT_ASSEM_ID = db.Column(db.String)

    # CREATE
    # TABLE
    # t_docking_lis_log(
    # ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    # ORDER_ID INT NOT NULL,
    # ASSEMS VARCHAR(500),
    # ASSEM_NAME VARCHAR(200),
    # IS_SUCCESS VARCHAR(10),
    # OP VARCHAR(50),
    # MSG VARCHAR(4096),
    # CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP --  创建记录时间，默认值为当前时间


class DockingLisLog(db.Model):
    # 体检结果接收日志表
    __tablename__ = 't_docking_lis_log'
    ID = db.Column(db.Integer, primary_key=True)
    ORDER_ID = db.Column(db.String)
    ASSEMS = db.Column(db.String)
    ASSEM_NAME = db.Column(db.String)
    IS_SUCCESS = db.Column(db.BOOLEAN)
    OP = db.Column(db.String)
    MSG = db.Column(db.String)

class ElementAssemSub(db.Model):
    """
      体检项目组表
    """
    __tablename__ = 't_element_assem_sub'
    ID = db.Column(db.Integer,primary_key=True)
    DEPARTMENT_ID = db.Column(db.Integer)
    NAME = db.Column(db.String)