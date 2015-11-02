select * from ProxyIP where checkedts=0;
-- insert into ProxyIP (proxyip,port,protocol,description,live,checkeddt,checkedts,checkcount,createdt,createts)
-- 	values("211.222.10.123",8000,"for test",1,)
insert into ProxyIP (proxyip,port,protocol,description,live,createdt,createts)values("211.222.10.123",8000,0,"for test",1,"2015-10-26","0")