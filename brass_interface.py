# coding=utf-8
import sys

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

import json

_DBG = False


# NOTE: to kill the websocket!!!
# sous windows:
#  netstat -ano|findstr 8888 (or other port number)
# -> le pid
# tskill pid


#  dictionnary of command, note : if a command is already in the dictionnary the new value replace the old one!
list_cmd = {}
# a single list of 112 binary (TODO: mettre un rateau de bit!!
list_resp = []

isKilled = False

#  add a new command in the dictionnary
# CALLED BY WebSocketHandler.on_command()
# cmd must be {'order':param}
def setcommand(cmd):
	global list_cmd
	list_cmd.update(cmd)
	#print "**************************************************"
	if _DBG: print "__DEBUG brass_interface." + sys._getframe().f_code.co_name + " : list_cmd waiting = " + str(list_cmd)
	#print "**************************************************"
	return


#  send the list of command (dictionnary)
# CALLED BY brass_process.brasserie
def getcommand():
	if list_cmd:
		ret = list_cmd.copy()
		list_cmd.clear()
	else:
		ret = {}
	if _DBG: print "__DEBUG brass_interface." + sys._getframe().f_code.co_name + " :  command = " + str(ret)
	return ret


#  only the last response is usefull
# CALLED BY brass_process.brasserie
def setresp(resp):
	global list_resp
	list_resp = resp
	if _DBG: print "__DEBUG brass_interface." + sys._getframe().f_code.co_name + " : list_resp waiting = " + str(list_resp)
	return

0
#  send the first resp and remove it from the list
# CALLED BY WebSocketHandler.on_command()
def getresp():
	global list_resp
	if list_resp:
		ret = list_resp
	else:
		ret = []
	if _DBG: print "__DEBUG brass_interface." + sys._getframe().f_code.co_name + " :  response = " + str(ret)
	return ret


def init_server(port):
	ws_app = Application()
	server = tornado.httpserver.HTTPServer(ws_app)
	server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
	return

def terminate():
	#TODO comment killer le webserver?????
	return

class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def check_origin(self, origin):
		return True

	def open(self):
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : open"
		pass

	def on_message(self, message):
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : on_message: " + message
		setcommand(json.loads(message))
		self.write_message(json.dumps(getresp()))

	def on_close(self):
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : close"
		pass


class IndexPageHandler(tornado.web.RequestHandler):
	def get(self):
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : get"
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
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : app tornado"

