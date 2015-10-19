#!/usr/bin/env python

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import io
class HttpServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.process()
		print self.path
	def process(self):
		content = ""
		print self.path

		enc = "UTF-8"
		content = content.encode(enc)
		f = io.BytesIO()
		f.write(content)
		f.seek(0)
		self.send_response(200)
		self.send_header("Content-type","text/html;charset=%s"%enc)
		self.send_header("Content-Length",str(len(content)))
		self.end_headers()
		print self.client_address
		print self.server.server_address
		# shutil.copyfileobj(f,self.wfile)

server = HTTPServer(("",8000),HttpServerHandler)
server.serve_forever()