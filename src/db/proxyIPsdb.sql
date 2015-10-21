CREATE TABLE ProxyIPs.ProxyIP(
	id			INT 		PRIMARY KEY NOT NULL,
	proxyip		CHAR(16)	NOT NULL,
	port 		INT 		NOT NULL,
	protocol	INT			NOT NULL,
	description	TEXT,
	live		TINYINT		NOT NULL DEFAULT 0,
	checkeddt	DATETIME	NOT NULL DEFAULT 0,
	checkedts	INT			NOT NULL DEFAULT 0,
	checkcount	INT			NOT NULL DEFAULT 0,
);