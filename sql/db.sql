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