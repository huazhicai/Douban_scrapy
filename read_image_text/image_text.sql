DROP TABLE IF EXISTS `image_text`;

CREATE TABLE image_text(
id int(11) unsigned not null auto_increment,
im varchar(64) null,
resize varchar(64) null,
im_detail varchar(64) null,
im_sharpen varchar(64) null,
en_sharpen varchar(64) null,
en_brightness varchar(64) null,
shap_bright varchar(64) null,
bright_shap varchar(64) null,
primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;