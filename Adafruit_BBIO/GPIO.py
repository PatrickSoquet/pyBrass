# ugly STUBS for EV only!!
import testpc
import brass_EV

# to avoid the loading of brass_proc which is not instancied in the case of a simple test
_TESTPC = True

def setup(gpio_open, IN):
	return None


def input(gpio):
	"""
	@type gpio: brass_EV.ev.gpio_open
	"""
	# to access EV instance: brass_testpc.brass_proc
	if _TESTPC:
		for ii in range(0, 6):
			if gpio in brass_EV.evs.GPIO_PINS[ii]:
				if gpio == brass_EV.evs.GPIO_PINS[ii][0]:  # the "open" circuit
					# answer 0 if close 1 if open
					return testpc.brass_proc.r_ev[ii]
					#brass_testpc.testpc.schedule[brass_testpc.testpc.timer_i][9 + ii]
				else:   # the "closed" circuit,
					# answer 0 if open 1 is close
					return not testpc.brass_proc.r_ev[ii]
					#brass_testpc.testpc.schedule[brass_testpc.testpc.timer_i][9 + ii]

		print "ERROR IN THE GPIO STUB!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	return None


def IN():
	return None
