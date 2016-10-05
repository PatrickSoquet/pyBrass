# coding=utf-8
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json


def possible():
	print "ggggggggggggggggggggggggggggggggggggggggggggggggggggggg"
	return

class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def check_origin(self, origin):
		return True

	def open(self):
		print("DBG: open")
		pass

	def on_message(self, message):
		print("DBG: on_message: " + message)
		# self.write_message("Your message was: " + message)
		# remplir l'état de la brasserie!!
		# FORMAT:
		# 1 pour 0 (le tableau va de 1 a 111)
		# 11 	(cuveau b)
		# 11 +10	( cuvebrass b +o)
		# 11 + 10 (cuvebu b+ o)
		# 6	(reverdoir b)
		# 22   	(t: b- v / b - v / b - v / b - v / b - v - o / b - v - o / b - v - o / b - v - o / b - v /
		# 16    (ev: b - cl / b - cl / b - cl - o / b - cl - o / b - cl - o / b - cl - o / )
		# 8	(m: off/ on x4)
		# 6	(r: off/ on x3)
		#
		# [0,
		#  1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
		#  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		#     0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
		#  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		#     0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
		#  1, 0, 0, 0, 0, 1,
		#  0, 1, 0, 1, 1, 0, 1, 0,
		#  0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0,
		#  0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0,
		#  1, 0, 0, 1, 0, 1, 0, 0,
		#  0, 1, 1, 0, 0, 1]

		possible()
		self.write_message(json.dumps([0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,1,0,0,0,1,1,0,0,1]))

#		self.write_message(json.dumps([0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1]))

	def on_close(self):
		print("DBG: close")
		pass


class IndexPageHandler(tornado.web.RequestHandler):
	def get(self):
		print("DBG: get")
		self.render("index.html")


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', IndexPageHandler),
			(r'/websocket', WebSocketHandler)
		]

		settings = {
			'template_path': 'templates'
		}
		tornado.web.Application.__init__(self, handlers, **settings)
		print("app tornado")


ws_app = Application()
server = tornado.httpserver.HTTPServer(ws_app)
server.listen(8888)
tornado.ioloop.IOLoop.instance().start()

