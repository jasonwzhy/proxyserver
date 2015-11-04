CREATE TABLE ProxyIP(
	id			INTEGER 	PRIMARY KEY AUTOINCREMENT,	
	proxyip		CHAR(16)	NOT NULL,	#代理IP
	port 		INT 		NOT NULL,	#代理端口
	protocol	INT			NOT NULL DEFAULT 0,
	location	INT 		NOT NULL DEFAULT 0,
	description	TEXT,
	live		TINYINT		NOT NULL DEFAULT 0,
	checkeddt	DATETIME	NOT NULL DEFAULT 0,
	checkedts	INT			NOT NULL DEFAULT 0,
	checkcount	INT			NOT NULL DEFAULT 0,
	createdt	DATETIME	NOT NULL DEFAULT (datetime('now', 'localtime')),
	createts	INT			NOT NULL DEFAULT (strftime('%s','now'))
);
#protocol 0-HTTP 1-HTTPS
#location 0-china 1-foreign