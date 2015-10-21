# proxyserver
一个代理server



功能模块分为

请求服务
	|------不断装载代理handler并请求CheckServer


HTTPServer
	|
	|---CheckServer
	|		|------只要有ip就激活库中纪录
	|---ProxyServer
	|		|------提供获得代理IP的API
			|------对代理IP进行增删API

SQLite
	|----IP代理数据库

tips:
	#1.Server同时监听http https以便区分请求协议
	#2.对于不同的协议使用不同的Handle绑定
	#3.Server需要生成证书加载至SSLContext
	ex:	openssl genrsa > privkey.pem
		openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1000



	#4.请求服务需要关闭ssl验证