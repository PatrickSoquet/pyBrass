# coding=utf-8

import brass_EV as EV
import brass_SENSOR as SENSOR
import brass_PID as PID
from smbus import SMBus
import Adafruit_BBIO.GPIO as GPIO
import time
#be able to test:
#   SENSOR:
#       take the value of any of the 4 sensor               => testsensor(0(uart),1,2,3)
#
#   EV:
#       to test open/close + real value of any of the 6 EV  => testev(0,1,2,3,4,5)
#
#   ACTUATOR:
#       to test the 4 last relays!                          => testactu(0,3) (=??)

adc = SENSOR.sensor_ADC()

def testsensor(param):
	# param: (0(uart),1 Volt cuve ebu,2 amp cuve eau,3 amp cuve ebu)
	if param == 0:
		rever = SENSOR.s_reverdoir()
		return rever.getVol()
	else:

		if param == 1:
			sen = SENSOR.s_cuvebu(adc)
			return sen.getVol()
		if param == 2:
			sen = SENSOR.s_cuvebu(adc)
			return sen.getWeight()
		if param == 3:
			sen = SENSOR.s_cuveau(adc)
			return sen.getVol()
	return


def testev(param):
	actu = EV.actuator()
	evtt = EV.ev(param, EV.evs.GPIO_PINS[param], actu)
	time.sleep(5)
	evtt.check()
	evtt.open()
	time.sleep(5)
	evtt.check()
	evtt.close(True)
	time.sleep(5)
	evtt.check()
	evtt.open()

	return


def testactu(param):
	actu = EV.actuator()
	if param == 0:
		actu.pump_off(force=True)
		actu.pump_on(force=True)
	elif param == 1:
		actu.recircul_off(force=True)
		actu.recircul_on(force=True)
	elif param == 2:
		actu.mixer_off(force=True)
		actu.mixer_on(force=True)
	elif param == 3:
		actu.alarm_off(force=True)
		actu.alarm_on(force=True)
	return


def testpid(param):
	pid = PID()
	pid.init_all_pid()
	return



#GPIO.setup("P8_11", GPIO.IN)
#GPIO.setup("P8_12", GPIO.IN)
#print GPIO.input("P8_11")
#print GPIO.input("P8_12")

testsensor(1)
testsensor(2)
testsensor(3)
#testactu(1)
#testev(0)
#testev(5)
#adc = SENSOR.sensor_ADC()
#senebu = SENSOR.s_cuvebu(adc)
#seneau = SENSOR.s_cuveau(adc)
#print senebu.getVol()
#print senebu.getWeight()
#print seneau.getVol()
# i2c = SMBus(1)
# print i2c.read_i2c_block_data(0x68,0x98,4)
# time.sleep(0.1)
# print i2c.read_i2c_block_data(0x68,0x98,4)
# print i2c.read_i2c_block_data(0x68,0xB9,4)
# time.sleep(0.1)
# print i2c.read_i2c_block_data(0x68,0xB9,4)
# print i2c.read_i2c_block_data(0x68,0xD9,4)
# time.sleep(0.1)
# print i2c.read_i2c_block_data(0x68,0xD9,4)
#
# adc = SENSOR.sensor_ADC()
# sen = SENSOR.s_cuveau(adc)
# moy = 0
# max = 1000
# for ii in range(0,max,1):
# 	moy += sen.getRawVol()
# print moy
# print moy/max
