-- 记录个人项目组状态（体检状态、收费）变化

DROP TABLE IF EXISTS t_personal_assem_changed;

CREATE TABLE t_personal_assem_changed (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ORDER_ID INT NOT NULL,
    ELEMENT_ASSEM_ID INT NOT NULL,
    UNIT_OR_OWN VARCHAR (20 ) NOT NULL, -- 公费或自费
    COST_STATUS VARCHAR ( 20 ) NOT NULL,-- 收费状态(未收、已收)
    EXAM_STATUS VARCHAR ( 20 ) NOT NULL,-- 体检状态(同体检状态)
    ASSEM_STATUS VARCHAR ( 20 ) NOT NULL,-- 项目组状态(新增、修改、删除)
    DIFFPRICE_STATUS VARCHAR(20) , -- 是否补差价(是,否)，默认为否
    DIFFPRICE_COST_STATUS VARCHAR(20), -- 补差价是否收费（已收、未收）
    OP_ID INT NOT NULL,-- 操作员ID
    CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP --  创建记录时间，默认值为当前时间

) ENGINE MYISAM;

CREATE INDEX idx_personal_assem_changed_orderid_assem_id ON t_personal_assem_changed ( ORDER_ID, ELEMENT_ASSEM_ID );

grant select on t_personal_assem_changed to 'third'@'%';

------------------------------------------------------------------------------------------------------------------------

-- LIS状态回传表

DROP TABLE IF EXISTS t_docking_lis_following;
CREATE TABLE t_docking_lis_following (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    YLJGDM VARCHAR ( 100 ) NOT NULL,-- 检验机构代码
    SQJGDM VARCHAR ( 100 ) NOT NULL,-- 申请机构代码
    SYSDM VARCHAR ( 100 ),-- 检验分配给各家机构的代码
    BRID VARCHAR ( 32 ),-- 病人唯一号/档案号
    SQDH VARCHAR ( 100 ) NOT NULL,--  医院内部唯一号码
    YWLSH VARCHAR ( 64 ),-- 门诊检验单则是医生就诊流水号，住院为住院流水号
    MZBZ VARCHAR ( 1 ),-- 门诊住院标志,1门诊2住院3体检4其他
    SJTM VARCHAR ( 32 ),-- 送检条码
    ZXTM VARCHAR ( 32 ) NOT NULL,-- 中心条码
    BRXM VARCHAR ( 100 ),-- 病人姓名
    BRXB VARCHAR ( 2 ),-- 病人性别 0未知的性别1男性2女性9未说明的性别
    BRNL VARCHAR ( 8 ),-- 年龄^单位格式，如 22^岁或者22^天
    SJRQ DATETIME NOT NULL,-- 送检日期
    JYLXBM VARCHAR ( 4 ),-- 检验类型编码   01	一般检查  02	血液类 03	生化类 04	免疫类 05	PCR类 06	微生物类 07	分子遗传类 08	病理类 99	其他类
    BGDMC VARCHAR ( 256 ),-- 必填。如“血常规”、尿常夫等写中文。
    ZTBZ VARCHAR ( 1 ) NOT NULL,-- 状态标志 1准备中 2检测中 3检测完成 4其他
    TOKEN VARCHAR ( 128 ) NOT NULL --  安全密钥

);
GRANT SELECT,DELETE,UPDATE,INSERT ON t_docking_lis_following TO 'third' @'%';

------------------------------------------------------------------------------------------------------------------------

-- PACS状态回传
DROP TABLE
IF
	EXISTS t_docking_pacs_following;
CREATE TABLE t_docking_pacs_following (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    YLJGDM VARCHAR ( 100 ) NOT NULL,-- 检验机构代码
    SQJGDM VARCHAR ( 100 ) NOT NULL,-- 申请机构代码
    BRID VARCHAR ( 32 ),-- 病人唯一号/档案号
    SQDH VARCHAR ( 100 ) NOT NULL,--  医院内部唯一号码
    YWLSH VARCHAR ( 64 ),-- 门诊检验单则是医生就诊流水号，住院为住院流水号
    MZBZ VARCHAR ( 1 ),-- 门诊住院标志,1门诊2住院3体检4其他
    JCXM VARCHAR ( 32 ),-- 检查项目代码
    BRXM VARCHAR ( 100 ),-- 病人姓名
    BRXB VARCHAR ( 2 ),-- 病人性别 0未知的性别1男性2女性9未说明的性别
    BRNL VARCHAR ( 8 ),-- 年龄^单位格式，如 22^岁或者22^天
    JCSJ DATETIME,-- 检查时间
    JCMC VARCHAR ( 64 ),-- 检查名称
    ZTBZ VARCHAR ( 1 ) NOT NULL,-- 状态标志  1已登记 2已预约3已检查4已审核5登记已取消6预约已取消
    TPDQDZ VARCHAR ( 512 ),-- 图片调取地址
    TWBGWJLLDZ VARCHAR ( 512 ),-- 图文报告文件浏览地址
    TOKEN VARCHAR ( 128 ) NOT NULL --  安全密钥

);
GRANT SELECT
	,
	DELETE,
	UPDATE,
INSERT ON t_docking_pacs_following TO 'third' @'%';

------------------------------------------------------------------------------------------------------------------------


-- 检验项目字典表
DROP TABLE
IF
	EXISTS t_docking_lis_dict;
CREATE TABLE t_docking_lis_dict (
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        YLJGDM VARCHAR ( 100 ) NOT NULL,-- 检验机构代码
        SYSDM VARCHAR ( 100 ) NOT NULL,-- 检验分配给各家机构的代码
        YBMLBM VARCHAR(20), -- 医保统编代码
        XMWSDM VARCHAR(20), -- 卫生收费代码
        XMMC VARCHAR(100) NOT NULL, -- 项目名称
        XMBM VARCHAR(100), -- 项目编码
        SFDW VARCHAR(64), -- 收费单位
        SFDJ DECIMAL(10,2),  -- 收费单价
        SFXDLB VARCHAR(2), -- 收费项目类别 1：医用材料；9：其他
        SYBZ VARCHAR(2), -- 使用标志,1.停用;  0.使用中
        YNZJBZ VARCHAR(1), -- 0.非自制；1.自制
        TBSM VARCHAR(100), -- 分类上或使用上的特别说明
        BZSM VARCHAR(100), -- 备注说明
        SQJGDM VARCHAR(100), -- 申请医疗机构代码
        XGBZ VARCHAR(1), --  修改标识 1 修改 2 新增 3 停用(3在影像接口里面不使用)
        TOKEN VARCHAR(128) -- 安全密钥
);

create index idx_docking_lis_dict_xmbm on t_docking_lis_dict (XMBM);


GRANT SELECT
	,
	DELETE,
	UPDATE,
INSERT ON t_docking_lis_dict TO 'third' @'%';

------------------------------------------------------------------------------------------------------------------------
-- 检查类项目字典表
DROP TABLE
IF
	EXISTS t_docking_pacs_dict;
CREATE TABLE t_docking_pacs_dict (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    YLJGDM VARCHAR ( 100 ) NOT NULL,-- 检验机构代码
    YYZBDM VARCHAR ( 100 ) NOT NULL,-- 医院自编代码
    YBMLBM VARCHAR(20), -- 医保统编代码
    XMWSDM VARCHAR(20), -- 卫生收费代码
    JCLX VARCHAR(32), -- 检查类型 01计算机X线断层摄影[CT] 02核磁共振成像[MR] 03数字减影血管造影[DSA] 04普通X光摄影[X-Ray] 05特殊X光摄影[X-Ray] 06超声检查[US] 07病理检查[Microscopy] 08內窥镜检查[ES] 09核医学检查[NM] 10其他检查[OT] 11心电检查 12 PETME 13 PETCT 备注：目前影像使用(MG、MR、PETMR、PETCT、CT、DX 、US)

    XMMC VARCHAR(100) NOT NULL, -- 项目名称
    XMBM VARCHAR(100), -- 项目编码
    JCBW VARCHAR(32), -- 文字说明被检查的部位。或活检部位
    BWBM VARCHAR(32), -- 检查部位ACR编码,表明病人的检查部位的编码（见附件 ACR ACR部位编码），多个部位，则位，编码中间用“,”分隔

    SFDW VARCHAR(64), -- 收费单位
    SFDJ DECIMAL(10,2),  -- 收费单价
    SFXDLB VARCHAR(2), -- 收费项目类别 1：医用材料；9：其他
    SYBZ VARCHAR(2), -- 使用标志,1.停用;  0.使用中
    YNZJBZ VARCHAR(1), -- 0.非自制；1.自制
    TBSM VARCHAR(100), -- 分类上或使用上的特别说明
    BZSM VARCHAR(100), -- 备注说明
    SQJGDM VARCHAR(100), -- 申请医疗机构代码
    XGBZ VARCHAR(1), --  修改标识 1 修改 2 新增 3 停用(3在影像接口里面不使用)
    TOKEN VARCHAR(128) -- 安全密钥
);
-- create index idx_docking_pacs_dict_xmbm on t_docking_pacs_dict (XMBM);

GRANT SELECT
	,
	DELETE,
	UPDATE,
INSERT ON t_docking_pacs_dict TO 'third' @'%';

------------------------------------------------------------------------------------------------------------------------

-- LIS危急值结果流水表

DROP TABLE IF EXISTS t_docking_lis_wjz_following;
CREATE TABLE t_docking_lis_wjz_following (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    YLJGDM VARCHAR ( 100 ) NOT NULL,-- 检验机构代码
    SQJGDM VARCHAR ( 100 ) NOT NULL,-- 申请机构代码
    SYSDM VARCHAR ( 100 ),-- 检验分配给各家机构的代码
	SQDH  VARCHAR(100), -- 申请单号,医院内部唯一号码(如果有多个用|分开，单个长度不超过12位，总长不超过100位)
    BRID VARCHAR ( 32 ),-- 病人唯一号/档案号
	BRXM VARCHAR ( 100 ) NOT NULL,-- 病人姓名
    BRXB VARCHAR ( 2 ),-- 病人性别 0未知的性别1男性2女性9未说明的性别
    BRNL VARCHAR ( 8 ),-- 年龄^单位格式，如 22^岁或者22^天
    LXDH VARCHAR(32), -- 联系电话
    JTDZ VARCHAR(128), -- 家庭地址
    YWLSH VARCHAR ( 64 ),-- 门诊检验单则是医生就诊流水号，住院为住院流水号
    MZBZ VARCHAR ( 1 ),-- 门诊住院标志,1门诊2住院3体检4其他
    BBLX VARCHAR(200), -- 标本类型
    JYTM VARCHAR(100), -- 检验条码
    SFXMDM VARCHAR(32), -- 收费项目代码,项目组
    SFXMMC VARCHAR(64), -- 收费项目名称
    XH VARCHAR(64), -- 序号
    XMDM VARCHAR(32), -- 检验明细编码
    XMMC VARCHAR(64), -- 检验明细名称
    JCJG VARCHAR(250), -- 量化结果或定性结果；例如“阴性”或者"+",以及描述性文字
    JLDW VARCHAR(64), -- 计量单位
    CKFW VARCHAR(1000), -- 参考范围A
    YCTS VARCHAR(1), -- 异常提示 1正常2无法识别的异常3异常偏高4异常偏低
    WJZBZ VARCHAR(10), -- 危急值标志 1-危急值；
    SBM VARCHAR(32), -- 记录的唯一标识，用于HIS处理后回馈给检验机构时，检验机构做对应更新,危急值识别码
    BZ VARCHAR(1000), -- 备注
	TOKEN VARCHAR ( 128 ) NOT NULL --  安全密钥

);
GRANT SELECT,DELETE,UPDATE,INSERT ON t_docking_lis_wjz_following TO 'third' @'%';

------------------------------------------------------------------------------------------------------------------------
-- 影像危急值（审核中）

DROP TABLE IF EXISTS t_docking_pacs_wjz_following;
CREATE TABLE t_docking_pacs_wjz_following (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    YLJGDM VARCHAR ( 100 ) NOT NULL,-- 检验机构代码
    SQJGDM VARCHAR ( 100 ) NOT NULL,-- 申请机构代码
	SQDH  VARCHAR(100), -- 申请单号,医院内部唯一号码(如果有多个用|分开，单个长度不超过12位，总长不超过100位)
    BRID VARCHAR ( 32 ),-- 病人唯一号/档案号
	BRXM VARCHAR ( 100 ) NOT NULL,-- 病人姓名
    BRXB VARCHAR ( 2 ),-- 病人性别 0未知的性别1男性2女性9未说明的性别
    BRNL VARCHAR ( 8 ),-- 年龄^单位格式，如 22^岁或者22^天
    LXDH VARCHAR(32), -- 联系电话
    JTDZ VARCHAR(128), -- 家庭地址
    YWLSH VARCHAR ( 64 ),-- 门诊检验单则是医生就诊流水号，住院为住院流水号
    MZBZ VARCHAR ( 1 ),-- 门诊住院标志,1门诊2住院3体检4其他
    YXHM VARCHAR(64), -- 影像号码
    JCXM VARCHAR(32), -- 检查项目代码
    JCSJ DATETIME, -- 检查时间
    JCLX VARCHAR(32), -- 检查类型,检查类型 01计算机X线断层摄影[CT] 02核磁共振成像[MR] 03数字减影血管造影[DSA] 04普通X光摄影[X-Ray] 05特殊X光摄影[X-Ray] 06超声检查[US] 07病理检查[Microscopy] 08內窥镜检查[ES] 09核医学检查[NM] 10其他检查[OT] 11心电检查 12 PETME 13 PETCT 备注：目前影像使用(MG、MR、PETMR、PETCT、CT、DX 、US)
    XMDM VARCHAR(32), -- 院内编码
    JCBW VARCHAR(32), -- 检查部位,文字说明被检查的部位。或活检部位
    BWBM VARCHAR(32), -- 检查部位ACR编码
    JCMC VARCHAR(64), -- 检查名称
    YYBZ VARCHAR(1), -- 0未做1阴性2阳性
    YXBX VARCHAR(2048), -- 影像表现或检查所见
    JCTS VARCHAR(1024), -- 检查诊断或提示
    JYBZ VARCHAR(1024), -- 建议或备注
    WJZBZ VARCHAR(10), -- 危急值标志,1-危急值
    SBM VARCHAR(32), -- 危急值识别码,记录的唯一标识，用于HIS处理后回馈给影像机构时，影像机构做对应更新
    BZ VARCHAR(1000), -- 备注
    TOKEN VARCHAR ( 128 ) NOT NULL --  安全密钥

);
GRANT SELECT,DELETE,UPDATE,INSERT ON t_docking_pacs_wjz_following TO 'third' @'%';

------------------------------------------------------------------------------------------------------------------------

-- 对接使用的条码变化流水表

DROP TABLE
IF
	EXISTS t_docking_barcode_changed;
CREATE TABLE t_docking_barcode_changed (
		ID BIGINT NOT NULL auto_increment PRIMARY KEY,
		ORDER_ID INT NOT NULL,
		BARCODE_ID bigint NOT NULL,
		BARCODE_ASSEM_TYPE_ID INT NOT NULL,
		ASSEM_SHORT_NAMES VARCHAR(500) NOT NULL,
		DELIVERY_SYMBOL VARCHAR ( 4 ) NOT NULL,
		INITIATOR INT NOT NULL,
		INITIAL_TIME datetime NOT NULL,
		OP_TYPE VARCHAR ( 10 ) NOT NULL,-- 操作类型 有新增、修改、删除
		CHANGE_USER INT,
		CHANGE_TIME datetime,
		REQ_NO VARCHAR ( 100 ),-- 申请单号
		REQ_TIME datetime,-- 申请时间
		REQ_STATUS VARCHAR ( 10 ),-- 申请状态,0为失败 1为成功
		REQ_MSG VARCHAR ( 1000 ) -- 申请返回的消息

);
CREATE INDEX idx_docking_barcod_changed_order_id ON t_docking_barcode_changed ( ORDER_ID );
CREATE INDEX idx_docking_barcod_changed_req_no ON t_docking_barcode_changed ( REQ_NO );
GRANT SELECT
	,
	DELETE,
	UPDATE,
INSERT ON t_docking_barcode_changed TO 'third' @'%';




drop TRIGGER if EXISTS tr_barcode_insert;

create TRIGGER tr_barcode_insert
after insert on t_barcode
for each row
begin
  insert into t_docking_barcode_changed (ORDER_ID,BARCODE_ID,BARCODE_ASSEM_TYPE_ID,ASSEM_SHORT_NAMES,DELIVERY_SYMBOL,INITIATOR,INITIAL_TIME,OP_TYPE,CHANGE_USER,CHANGE_TIME)
	VALUES (NEW.ORDER_ID,NEW.ID,NEW.BARCODE_ASSEM_TYPE_ID,NEW.ASSEM_SHORT_NAMES,NEW.DELIVERY_SYMBOL,NEW.INITIATOR,NEW.INITIAL_TIME,'新增',NEW.CHANGE_USER,NEW.CHANGE_TIME);
end;


drop TRIGGER if EXISTS tr_barcode_update;

create TRIGGER tr_barcode_update
after update on t_barcode
for each row
begin
  insert into t_docking_barcode_changed (ORDER_ID,BARCODE_ID,BARCODE_ASSEM_TYPE_ID,ASSEM_SHORT_NAMES,DELIVERY_SYMBOL,INITIATOR,INITIAL_TIME,OP_TYPE,CHANGE_USER,CHANGE_TIME)
	VALUES (NEW.ORDER_ID,NEW.ID,NEW.BARCODE_ASSEM_TYPE_ID,NEW.ASSEM_SHORT_NAMES,NEW.DELIVERY_SYMBOL,NEW.INITIATOR,NEW.INITIAL_TIME,'修改',NEW.CHANGE_USER,NEW.CHANGE_TIME);
end;


drop TRIGGER if EXISTS tr_barcode_delete;

create TRIGGER tr_barcode_delete
after delete on t_barcode
for each row
begin
  insert into t_docking_barcode_changed (ORDER_ID,BARCODE_ID,BARCODE_ASSEM_TYPE_ID,ASSEM_SHORT_NAMES,DELIVERY_SYMBOL,INITIATOR,INITIAL_TIME,OP_TYPE,CHANGE_USER,CHANGE_TIME)
	VALUES (OLD.ORDER_ID,OLD.ID,OLD.BARCODE_ASSEM_TYPE_ID,OLD.ASSEM_SHORT_NAMES,OLD.DELIVERY_SYMBOL,OLD.INITIATOR,OLD.INITIAL_TIME,'删除',OLD.CHANGE_USER,OLD.CHANGE_TIME);
end;


------------------------------------------------------------------------------------------------------------------------
-- 通过样本号查询项目信息视图

DROP VIEW IF EXISTS v_docking_lis_request_view;
CREATE VIEW v_docking_lis_request_view AS SELECT
        concat( barcode.ORDER_ID, '-', element.id ) AS ID,
        barcode.ID AS BARCODE_ID,
        barcode.ORDER_ID,
        barcodedetail.ELEMENT_ASSEM_ID,
        barcodeclass.SPECIMEN_TYPE,
        specimen_dict.BASE_VALUE SPECIMEN_TYPE_NAME,
        assem.EXTERNAL_SYS_CONTROL_CODE ASSEM_CODE,
        assem.`NAME` ASSEM_NAME,
        element.EXTERNAL_SYS_CONTROL_CODE ELEMENT_CODE,
        element.`NAME` ELEMENT_NAME,
        person.USERNAME,
        person.SEX,
        porder.AGE,

        porder.INITIATOR,
		porder.INITIAL_TIME,
		person.BIRTHDAY,
        person.ADDRESS,
        person.TELEPHONE,
        person.CERT_TYPE,
        person.CERT_ID,
        porder.ARRIVAL_DATE,
        '体检中心' DEPARMENT
FROM
	t_barcode barcode
	INNER JOIN t_barcode_detail barcodedetail ON barcode.ID = barcodedetail.BARCODE_ID
	INNER JOIN t_barcode_assem_class barcodeclass ON barcode.BARCODE_ASSEM_TYPE_ID = barcodeclass.ID
	LEFT JOIN t_base_dict specimen_dict ON barcodeclass.SPECIMEN_TYPE = specimen_dict.BASE_CODE
	AND specimen_dict.type = '标本类型'
	INNER JOIN t_element_assem_sub assem ON barcodedetail.ELEMENT_ASSEM_ID = assem.ID
	INNER JOIN t_element_assem_detail_sub assemdetail ON assem.ID = assemdetail.ELEMENT_ASSEM_ID
	INNER JOIN t_element_sub element ON assemdetail.ELEMENT_ID = element.ID
	INNER JOIN t_personal_order porder ON barcode.order_id = porder.id
	INNER JOIN t_person person ON porder.person_id = person.id;

GRANT SELECT ON
	v_docking_lis_request_view TO 'third' @'%';


------------------------------------------------------------------------------------------------------------------------
-- 项目变动通知流水表（视图),体检信息、收费都会变动

drop view if EXISTS v_docking_assems_changed;

create view  v_docking_assems_changed as
SELECT
	assemchanged.ID,
	assemchanged.ORDER_ID,
	assemchanged.ELEMENT_ASSEM_ID,
	assemchanged.UNIT_OR_OWN,
	assemchanged.COST_STATUS,
	assemchanged.EXAM_STATUS,
	assemchanged.ASSEM_STATUS,
	assemchanged.OP_ID,
	assemchanged.DIFFPRICE_STATUS,
	assemchanged.DIFFPRICE_COST_STATUS,
    assem.DEPARTMENT_ID,
    assem.NAME,
	assem.EXTERNAL_SYS_CONTROL_CODE ASSEM_CODE

FROM
	t_personal_assem_changed assemchanged
	inner join t_element_assem_sub assem on assemchanged.ELEMENT_ASSEM_ID = assem.ID;

	grant select on v_docking_assems_changed to 'third'@'%';


------------------------------------------------------------------------------------------------------------------------
-- 预约项目组表

DROP VIEW IF EXISTS v_docking_pacs_request_view;

CREATE VIEW v_docking_pacs_request_view AS SELECT
        concat( porder.ID, '-', element.id ) AS ID,
        porder.ID as ORDER_ID,
        passem.ELEMENT_ASSEM_ID,
        assem.EXTERNAL_SYS_CONTROL_CODE ASSEM_CODE,
        assem.`NAME` ASSEM_NAME,
        element.EXTERNAL_SYS_CONTROL_CODE ELEMENT_CODE,
        element.`NAME` ELEMENT_NAME,
		person.USERNAME,
        person.SEX,
        porder.AGE,
        porder.INITIATOR,
		porder.INITIAL_TIME,
		person.BIRTHDAY,
        person.ADDRESS,
        person.TELEPHONE,
        person.CERT_TYPE,
        person.CERT_ID,
        porder.ARRIVAL_DATE,
        '体检中心' DEPARMENT,
        assem.DEPARTMENT_ID
FROM
    t_personal_order porder
    INNER JOIN t_person person ON porder.person_id = person.id
	INNER JOIN t_person_element_assem passem on porder.id =  passem.order_id  and passem.symbol = '有效'
	INNER JOIN t_element_assem_sub assem ON passem.ELEMENT_ASSEM_ID = assem.ID
	INNER JOIN t_element_assem_detail_sub assemdetail ON assem.ID = assemdetail.ELEMENT_ASSEM_ID
	INNER JOIN t_element_sub element ON assemdetail.ELEMENT_ID = element.ID;

GRANT SELECT ON
	v_docking_pacs_request_view TO 'third' @'%';



------------------------------------------------------------------------------------------------------------------------

-- pacs数据平台上传日志表

DROP TABLE IF EXISTS t_docking_pacs_assem_log;

CREATE TABLE t_docking_pacs_assem_log (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ORDER_ID INT NOT NULL,
    USERNAME VARCHAR(50),
    SEX VARCHAR(10),
    AGE VARCHAR(10),
    ASSEM_ID INT NOT NULL,
    ASSEM_NAME VARCHAR(100),
    REQ_NO VARCHAR ( 100 ),-- 申请单号
    REQ_TIME datetime,-- 申请时间
    REQ_STATUS VARCHAR ( 10 ),-- 申请状态,0为失败 1为成功
    REQ_MSG VARCHAR ( 1000 ), -- 申请返回的消息
    CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP --  创建记录时间，默认值为当前时间

) ENGINE MYISAM;


create index idx_docking_pacs_assem_log_order_id on t_docking_pacs_assem_log
(
   order_id
);

create index idx_docking_pacs_assem_log_req_no on t_docking_pacs_assem_log
(
   req_no
);

grant select,insert,update,delete on t_docking_pacs_assem_log to 'third'@'%';

-----------------------------------------------------------------------------------
grant select on t_barcode_detail to 'third'@'%';






















