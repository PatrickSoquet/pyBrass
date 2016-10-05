# coding=utf-8
import threading
import time

import brass_process
import brass_interface
import testpc


_DBG = True
_TEST = True



def core(br):
	# br.initialize(input('Enter the name of the input file (without .ibf extension): '))
	if _DBG: print "__DEBUG CORE : initializing"

	br.ihmListInputFile()
	while br.pause:
		time.sleep(.200)
		br.ihm()
		pass
	br.initialize()
	if _DBG: print "__DEBUG CORE : begining of the brew"
	br.begin_brass()
	if _DBG: print "__DEBUG CORE : loop"
	while ((br.timer - br.begin_time) < 600 * 60) and (not br.quit_brass()):
		if _DBG: print "__DEBUG CORE : time = " + str(br.timer - br.begin_time)
		br.cycle()
		if br.restart:
			br.__init__()
			br.restart = False
			br.ihmListInputFile()
			if _TEST:
				testpc.testpc.init_static(br)
			while br.pause:
				time.sleep(.200)
				br.ihm()
				pass
			br.initialize()
			br.begin_brass()
	print "FINI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	brass_interface.terminate()
	return


def websocket(port):
	brass_interface.init_server(port)
	return


brass = brass_process.brasserie()
if _TEST:
	testpc.testpc.init_static(brass)


#thread 1:  core(brass)
threading.Thread(target=core, args=(brass,)).start()

#thread 2:  websocket(8894)
#threading.Thread(target=websocket, args=(8888,)).start()
# TODO brass_interface.init_server(8895) : gérer +1 server!! => communication avec  2 clients!! pas forcément la peine! voir si les 2 clients peuvent taper dans le même server!
websocket(8888)
