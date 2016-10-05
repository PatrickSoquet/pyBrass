# coding=utf-8
import brass_PID
import brass_EV
import brass_SENSOR
import brass_interface

import testpc
# import math
# import random
import time
import sys
import json
import os

_TEST = True
_TEST_PASAPAS = False
# !! _TEST or _TEST_PASAPAS
# only used as True to test on a PC with brass_test + stub for thee HW accessor
_DBG = True

CUVEAU_VOL_MAX = 73  # TODO verify!
CUVEAU_VOL_MIN_HOT = 20  # TODO verify!
CUVEAU_VOL_MIN_RECIRCUL = 10  # TODO verify!

REVERDOIR_VOL_MIN_HOT = 5  # TODO verify!

CUVEBU_VOL_MAX = 70  # TODO verify!
CUVEBU_VOL_MIN_HOT = 20  # TODO verify!


RECIRCUL_CONFIG_TIME = 20  # number of s during the time the recurculation of cuveau
RECIRCUL_CONFIG_FREQUENCY = 5  # find the word??? TODO


class brasserie:
	# pids
	# actu
	# evs
	# reverdoir_pump
	# cuveau_pump
	# mixer
	# general_alarm
	# adc
	# cuveau_sensor
	# cuvebu_sensor
	# reverdoir_sensor
	# r_temper
	# r_vol
	# r_SV
	# r_ev
	# timer



	def __init__(self):
		self.actu = brass_EV.actuator()
		self.adc = brass_SENSOR.sensor_ADC()

		self.pids = brass_PID.pid()
		self.evs = brass_EV.evs(self.actu)
		self.reverdoir_pump = brass_EV.pump(self.actu)
		self.cuveau_pump = brass_EV.recircul(self.actu)
		self.mixer = brass_EV.mixer(self.actu)      # note: the mixer can control can also control the pump for the cleaning cycle
		self.general_alarm = brass_EV.alarm(self.actu)
		self.cuveau_sensor = brass_SENSOR.s_cuveau(self.adc)
		self.cuvebu_sensor = brass_SENSOR.s_cuvebu(self.adc)
		self.reverdoir_sensor = brass_SENSOR.s_reverdoir()
		self.r_temper = [0] * 4  # cuveau / cuve brass / reverdoir / cuvebu
		self.r_SV = [0] * 4  # cuveau / cuve brass(non util) / reverdoir / cuvebu
		self.r_vol = [0] * 3  # cuveau / reverdoir / cuvebu
		self.r_vol_brass = 0  # calculated!!
		self.r_ev = [0] * 6  # entrée cuveau / sortie cuveau / entrée reverdoir / sortie reverdoir / entrée cuvébu sortie cuvebu # =0 for close / YES it is opposite to the 4 other actuator...
		self.r_cuveau_pump = 1   # =1 for off
		self.r_reverdoir_pump = 1  # =1 for off
		self.r_mixer = 1  # =1 for off
		self.r_alarm = 1  # =1 for off
		self.r_alarm_txt = ""  #
		self.timer = 0
		self.nbcycle = 0
		self.begin_time = 0

		self.outputfile = None
		self.inputfile = None

		self.next_order = None

		self.pause = True      #  True before the begining and when we make a pause...
		self.pausetimer = 0     # if we want to pause the timer too!!!! TODO a voir c omment implementer...

		self.restart = False

		# state & order of the brasserie

		self.cuveau_temp_target = 0
		self.isCuveauChauffe = False  # note : if False SV MUST be set to 0!!!! if True: any temperature

		self.isCuveauRemplissage = False  # flag danger si True???
		self.cuveau_vol_target = 0
		self.isCuveauVidage = False

		# cuve brass+reverdoir
		self.isReverdoirChauffe = False  # note : if False SV MUST be set to 0!!!! if True: any temperature
		self.cuvebrass_temp_target = 0
		self.reverdoir_temp_target = 0
		self.isMixer = False
		self.isReverdoirRecircul = False
		self.isCuveauForceRecircul = False
		# cuve ebu
		self.cuvebu_temp_target = 0
		self.cuvebu_vol_target = 0
		self.isCuvebuRemplissage = False
		self.isCuvebuChauffe = False  # note : if False SV MUST be set to 0!!!! if True: any temperature
		self.isCuvebuVidage = False
		#  Cuvebu_density_target = 0 # faut pas réver!!! d'abords tester la mesure de densité

		self.cleaning_process = False  # True if not brewing but only cleaning the brewerie

		self.listFile = ""
		self.inputfileContent1 = ""
		self.inputfileContent2 = ""
		self.isQuit = False
		return

	def initialize(self):
		#self.inputfile = open(input_file + ".ibf", 'r')   # input brewerie file, oui c'est naze...
		self.next_order = json.loads(self.inputfile.readline())
		if 'CLEANING_PROCESS' in self.next_order:
			self.cleaning_process = self.next_order.get("CLEANING_PROCESS")  # the second line is to know if it is just a cleaning, optionnal
			self.next_order = json.loads(self.inputfile.readline())

		self.outputfile = open(os.path.join(os.getcwd(), "output", os.path.split(self.inputfile.name)[1][:-4] + time.strftime('%y')+"_"+time.strftime('%m')+"_"+time.strftime('%d')+"_"+time.strftime('%H')+"h"+time.strftime('%M')+ ".obf"), 'w+')  # output brewerie file, c'est naze aussi...
		self.pids.init_all_pid()

		self.evs.close_all()
		self.evs.check_all()

		self.reverdoir_pump.off()
		self.cuveau_pump.off()
		self.mixer.off()

		self.general_alarm.off()

		# not needed anymore
		self.inputfileContent1 = ""
		self.inputfileContent2 = ""

		return

	def begin_brass(self):
		self.begin_time = int(time.time())
		self.timer = self.begin_time
		return

	def autotestempty(self):
		# test tout... vérifie les vannes (ouvre/ferme) + les niveaux (doit etre 0 partout...)
		# never use it if the brewerie is full of liquid!!!
		#
		print "full autotest ..."
		ret = self.evs.check_all()
		self.evs.open_all()
		ret = ret and self.evs.check_all()
		self.evs.close_all()

		ret = ret and self.pids.checkAll()

		ret = ret and self.cuveau_sensor.check()
		ret = ret and self.cuvebu_sensor.check()
		ret = ret and self.reverdoir_sensor.check()
		if ret: return 'Ok'
		else: return'ERROR'
	
	def autotest(self):
		#test tout en marche!: vérifie les vannes + les limites des niveaux
		print "autotest ..."
		ret = self.evs.check_all()
		ret = ret and self.pids.checkAll()
		ret = ret and self.cuveau_sensor.check()
		ret = ret and self.cuvebu_sensor.check()
		ret = ret and self.reverdoir_sensor.check()
		if ret:
			return 'Ok'
		else:
			return 'ERROR'

	def getData(self):
		# mets a jour les datas
		tmp = self.pids.read_all_temp_SV()
		self.r_temper = tmp[0]
		self.r_SV = tmp[1]
		self.r_vol[0] = self.cuveau_sensor.getVol()
		self.r_vol[1] = self.reverdoir_sensor.getVol()
		self.r_vol[2] = self.cuvebu_sensor.getVol()
		# ONLY FOR TESTING WITH STUBS!!! for the temperatures and the volumes!!
		if _TEST or _TEST_PASAPAS:
			tmp = testpc.testpc.getdata()
			self.r_temper = tmp[1:5]
			self.r_vol = tmp[5:8]
			#  self.r_temper = [testpc.testpc.getdata('r_temper_cuveau_0'), testpc.testpc.getdata('r_temper_cuve_brass_1'),testpc.testpc.getdata('r_temper_cuve_reverdoir_2'),testpc.testpc.getdata('r_temper_cuvebu_3')]
			#  self.r_vol[0] = testpc.testpc.getdata('r_vol_cuveau_0')
			#  self.r_vol[1] = testpc.testpc.getdata('r_vol_rev_1')
			#  self.r_vol[2] = testpc.testpc.getdata('r_vol_cuvebu_2')
		return

	def getAllData(self):
		#mets a jour TOUTES les data
		self.getData()
		self.r_ev = self.evs.getStateAll()
		self.r_cuveau_pump = self.cuveau_pump.getState()
		self.r_reverdoir_pump = self.reverdoir_pump.getState()
		self.r_mixer = self.mixer.getState()
		self.r_alarm = self.general_alarm.getState()
		self.r_alarm_txt = self.general_alarm.getMsg()
		return

	def reccord(self):
		#sauvegarde dans un fichier
		self.outputfile.write(str(self.nbcycle) + " " + str(self.timer) + " " + str(self.r_temper) + " " + str(self.r_SV) + " " + str(self.r_vol) + " " + str(self.r_vol_brass) + " " + str(self.r_ev) + " " + str(self.r_cuveau_pump) + " " + str(self.r_reverdoir_pump) + " " + str(self.r_mixer) + " " + str(self.r_alarm) + "\n")
		return

	# CUVEAU_FILL           vol
	def cuveau_fill(self, vol):
		# ne coupe pas la sortie!!!
		#remplit la cuve eau de vol en l
		self.isCuveauRemplissage = True
		self.cuveau_vol_target = vol
		if self.isCuveauVidage:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : !!!! fill the cuveau when still empty it, must not happen or impossible to calculate the volume of water added to the CUVE BRASS!!!"
		return

	# CUVEAU_HEAT           temp
	def cuveau_heat(self, temp):
		self.cuveau_temp_target = temp
		if temp != 0: self.isCuveauChauffe = True
		else: self.isCuveauChauffe = False
		return

	# CUVEBRASS_FILL        vol
	def cuvebrass_fill(self, vol):
		self.isCuveauVidage = True
		self.cuveau_vol_target = self.r_vol[0] - vol
		if self.cuveau_vol_target < 0:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : !!!! not enough water in CUVEAU to fill CUVE BRASS!!! lack " + str(self.cuveau_vol_target * -1) + "Liters!!"
		if self.isCuveauRemplissage:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : !!!! empty the cuveau when still fill it, must not happen or impossible to calculate the volume of water added to the CUVE BRASS!!!"
		return

	# REVERDOIR_HEAT            temp
	def reverdoir_heat(self, temp):
		self.reverdoir_temp_target = temp
		if temp != 0: self.isReverdoirChauffe = True
		else: self.isReverdoirChauffe = False
		return

	# REVERDOIR                 bool
	def reverdoir_recircul(self, isOn):
		self.isReverdoirRecircul = isOn
		return

	# CUVEAU_RECIRCUL                 bool
	def cuveau_recircul(self, isOn):
		self.isCuveauForceRecircul = isOn
		return

	# MIXER                     bool
	def mixer_onoff(self, isOn):
		self.isMixer = isOn
		return

	# CUVEBRASS_EMPTY           vol
	def cuvebrass_empty(self, vol):
		self.isCuvebuRemplissage = True
		self.cuvebu_vol_target = vol
		if self.isCuveauRemplissage:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : !!!! fill the cuvebu when still empty it, must not happen or impossible to calculate the volume of water added to the CUVE BRASS!!!"
		return

	# CUVEBU_HEAT               temp
	def cuvebu_heat(self, temp):
		self.cuvebu_temp_target = temp
		if temp != 0: self.isCuvebuChauffe = True
		else: self.isCuvebuChauffe = False
		return

	# CUVEBU_EMPTY              vol
	def cuvebu_empty(self, vol):
		self.isCuvebuVidage = True
		self.cuvebu_vol_target = vol
		if self.isCuveauRemplissage and not self.cleaning_process:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : !!!! empty the cuvebu when still fill it, must not happen or impossible to calculate the volume of water added to the CUVE BRASS!!!"
		return

	# ALARM                     bool
	def alarm_onoff(self, ison, txt):
		if ison:
			print "ALARM ON: " + txt
			#TODO faire passer ce txt a l'ihm!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			self.general_alarm.on("txt")
		elif not ison:
			print "ALARM OFF: " + txt
			self.general_alarm.off()
		return

	#empty the cuvebu in the cuveau or in the evier...
	# PUMP_EMPTY_CUVEBU         /
	def pump_empty_cuvebu(self):
		self.isCuvebuVidage = True
		self.cuvebu_vol_target = 0
		self.isCuvebuChauffe = False
		return

	def pauseonoff(self, p):
		self.pause = p
		return

	def cycle_cuveau(self):
		# verif cuveau
		# verif trop plein!!!
		if self.r_vol[0] > CUVEAU_VOL_MAX:
			self.evs.close(0)
			time.sleep(2)
			if self.evs.check(0) != 'Ok':
				print "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
				self.general_alarm.on("TODO: CRITICAL ALARM: la cuve d'eau va déborder!")
		if self.isCuveauChauffe:
			if self.r_vol[0] < CUVEAU_VOL_MIN_HOT:
				if _DBG: print "__WARNING " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : impossible to launch the heating of the cuveau: water volume = " + str(self.r_vol[0]) + "l, minimum volume is " + str(CUVEAU_VOL_MIN_HOT) + "l"
				self.pids.write_SV(0, 0)
				# mais nouveau changement : si cuveau se remplit OK winon alarme???
				# self.isCuveauChauffe = False   # finalement pas d'alarme! alumera la chauffe quand le volume sera sufisant!!
				# self.general_alarm.on()
			else:
				self.pids.write_SV(0, self.cuveau_temp_target)
			if self.r_vol[0] >= CUVEAU_VOL_MIN_RECIRCUL and (((self.timer / RECIRCUL_CONFIG_TIME) % RECIRCUL_CONFIG_FREQUENCY) == 0 or self.isCuveauForceRecircul):
				self.cuveau_pump.on()
			else:
				self.cuveau_pump.off()

			if self.cuveau_temp_target == 0:
				self.isCuveauChauffe = False
		else:
			self.pids.write_SV(0, 0)
			self.cuveau_pump.off()

		if self.isCuveauRemplissage:
			if self.r_vol[0] >= self.cuveau_vol_target:
				self.evs.close(0)
				self.isCuveauRemplissage = False
			else:
				self.evs.open(0)
		else:
			self.evs.close(0)
		if self.isCuveauVidage:
			if self.r_vol[0] == 0 or self.r_vol[0] <= self.cuveau_vol_target:
				self.evs.close(1)
				self.isCuveauVidage = False
			else:
				self.evs.open(1)
		else:
			self.evs.close(1)
		return

	def cycle_brass_rever(self):
		# note : pour l'instant pas de vérification que le reverdoir est bouché...

		# note le reverdoir permet de suivre une recette!! ne permet pas de coriger une temp trop basse d'empatage!! faudra le regler à la mano...

		if self.isReverdoirChauffe:
			if self.r_vol[1] < REVERDOIR_VOL_MIN_HOT:
				print "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
				self.pids.write_SV(2, 0)
				self.isReverdoirChauffe = False  # TODO: ca va poser un pb!!!  il faut pouvoir reinitiliser isReverdoirChauffe a True après reglage du problème!!
				self.general_alarm.on("TODO: CRITICAL ALARM: le reverdoir chauffe alors qu'il n'y a pas assez d'eau!!")
			self.pids.write_SV(2, self.reverdoir_temp_target)
		else:
			self.pids.write_SV(2, 0)

		if self.isReverdoirRecircul:
			self.evs.open(2)
			self.evs.open(3)
			self.reverdoir_pump.on()
		else:
			self.reverdoir_pump.off()
			self.evs.close(3)
			self.evs.close(2)

		if self.isMixer:
			self.mixer.on()
		else: self.mixer.off()
		return

	def cycle_ebu(self):
		if self.r_vol[2] > CUVEBU_VOL_MAX:
			self.evs.close(4)
			time.sleep(2)
			#if still open BIG PROBLEM, note : supposed to be impossible...
			if self.evs.getState(4):
				print "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
				self.general_alarm.on("TODO: CRITICAL ALARM: la cuve d'ébulition va déborder!!")
		if self.isCuvebuChauffe:
			if self.r_vol[2] < CUVEBU_VOL_MIN_HOT:
				if _DBG: print "__WARNING " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : impossible to launch the heating of the cuveau: water volume = " + str(self.r_vol[2]) + "l, minimum volume is " + str(CUVEBU_VOL_MIN_HOT) + "l"
				self.pids.write_SV(3, 0)
				# self.isCuvebuChauffe = False
				# self.general_alarm.on()
			self.pids.write_SV(3, self.cuvebu_temp_target)
			if self.cuvebu_temp_target == 0:
				self.isCuvebuChauffe = False
		else:
			self.pids.write_SV(3, 0)
		if self.isCuvebuRemplissage:
			if self.r_vol[2] >= self.cuvebu_vol_target:
				self.evs.close(4)
				self.isCuvebuRemplissage = False
			else:
				self.evs.open(4)
		else:
			self.evs.close(4)

		if self.isCuvebuVidage:
			#  of course ne pas lancer le vidage de la cuve!!! le faire a la main (d'ailleurs le bouton de l'EV6 doit toujours rester sur fermé-manuel
			# pour le mode lavage voir le cycle "cycle_lavage"
			print "ALARM FINISHed!!!!!!!!!!!!!!!!!!"
			# TODO envoyer un messge qui va bien!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			self.general_alarm.on("TODO: INFO ALARM: brassage terminé")
		return

#for cleaning only the following commands are used:
# chauffe CuveEau/ceuveebu/
# vidageCuvebu (-> evier ou cuveeau)
# vidageCuveau
# reverdoir
# vidage cuvebrass

	def cycle_cleaning(self):
		if self.isCuvebuChauffe:
			if self.r_vol[2] < CUVEBU_VOL_MIN_HOT:
				if _DBG: print "__WARNING " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : impossible to launch the heating of the cuveau: water volume = " + str(self.r_vol[2]) + "l, minimum volume is " + str(CUVEBU_VOL_MIN_HOT) + "l"
				self.pids.write_SV(3, 0)
				# self.isCuvebuChauffe = False
				# self.general_alarm.on()
			self.pids.write_SV(3, self.cuvebu_temp_target)
			if self.cuvebu_temp_target == 0:
				self.isCuvebuChauffe = False
		else:
			self.pids.write_SV(3, 0)

		if self.isCuveauChauffe:
			if self.r_vol[0] < CUVEAU_VOL_MIN_HOT:
				if _DBG: print "__WARNING " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : impossible to launch the heating of the cuveau: water volume = " + str(self.r_vol[0]) + "l, minimum volume is " + str(CUVEAU_VOL_MIN_HOT) + "l"
				self.pids.write_SV(0, 0)
				# self.isCuveauChauffe = False   # finalement pas d'alarme! alumera la chauffe quand le volume sera sufisant!!
				# self.general_alarm.on()
			self.pids.write_SV(0, self.cuveau_temp_target)
			if self.r_vol[0] >= CUVEAU_VOL_MIN_RECIRCUL and (
				(self.timer / RECIRCUL_CONFIG_TIME) % RECIRCUL_CONFIG_FREQUENCY) == 0:
				self.cuveau_pump.on()
			else:
				self.cuveau_pump.off()
			if self.cuveau_temp_target == 0:
				self.isCuveauChauffe = False
		else:
			self.pids.write_SV(0, 0)
			self.cuveau_pump.off()

		if self.isCuveauVidage and self.r_vol[0] > 1:
			self.evs.open(1)
		else:
			self.evs.close(1)

		if self.isCuvebuRemplissage:
			if self.r_vol[2] > CUVEBU_VOL_MAX:
				self.evs.close(4)
			else:
				self.evs.open(4)
		else:
			self.evs.close(4)

		if self.isCuvebuVidage:
			if self.r_vol[2] < 1:
				self.mixer.off()        # note : for the cleaning the mixer control the external pump!!!
				self.isCuvebuVidage = False
				self.evs.close(5)
				self.evs.close(0)
			else:
				self.evs.open(0)
				self.evs.open(5)
				self.mixer.on()  # note : for the cleaning the mixer control the external pump!!!
		else:
			self.mixer.off()
			self.evs.close(5)
			self.evs.close(0)

		if self.isReverdoirRecircul:
			self.evs.open(2)
			self.evs.open(3)
			self.reverdoir_pump.on()
		else:
			self.reverdoir_pump.off()
			self.evs.close(3)
			self.evs.close(2)
		return

	# CUVEAU_FILL               vol
	# CUVEAU_HEAT               temp
	# CUVEBRASS_EMPTY           vol
	# CUVEBRASS_FILL            vol
	# REVERDOIR_HEAT            temp
	# CUVEBU_EMPTY              vol
	# CUVEBU_HEAT               temp
	# REVERDOIR                 bool
	# MIXER                     bool
	# ALARM                     bool
	# PUMP_EMPTY_CUVEBU         /

	def order(self):
		chrono = self.timer - self.begin_time
		tim = self.next_order.get("TIME") * 60
		# pour debug pas a pas!!!
		if _TEST_PASAPAS:
			chrono = self.nbcycle
			tim /= 60
		if _TEST:
			tim /= 60
		if tim < chrono:   # TIME in minutes, chrono in second
			if "CUVEAU_FILL" in self.next_order: self.cuveau_fill(self.next_order.get("CUVEAU_FILL"))
			if "CUVEAU_HEAT" in self.next_order: self.cuveau_heat(self.next_order.get("CUVEAU_HEAT"))
			if "CUVEBRASS_FILL" in self.next_order: self.cuvebrass_fill(self.next_order.get("CUVEBRASS_FILL"))
			if "REVERDOIR_HEAT" in self.next_order: self.reverdoir_heat(self.next_order.get("REVERDOIR_HEAT"))
			if "CUVEBRASS_EMPTY" in self.next_order: self.cuvebrass_empty(self.next_order.get("CUVEBRASS_EMPTY"))
			if "CUVEBU_HEAT" in self.next_order: self.cuvebu_heat(self.next_order.get("CUVEBU_HEAT"))
			if "CUVEBU_EMPTY" in self.next_order: self.cuvebu_empty(self.next_order.get("CUVEBU_EMPTY"))
			if "REVERDOIR" in self.next_order: self.reverdoir_recircul(self.next_order.get("REVERDOIR"))
			if "MIXER" in self.next_order: self.mixer_onoff(self.next_order.get("MIXER"))
			if "ALARM" in self.next_order: self.alarm_onoff(True, self.next_order.get("ALARM"))
			if "PUMP_EMPTY_CUVEBU" in self.next_order: self.pump_empty_cuvebu()
			no = self.inputfile.readline()
			if no == '':
				return
			self.next_order = json.loads(no)
			# TODO  !!!! attention gérer la fin du fichier avec le readlines => gestion d'exception!!!
		return

	def ihm(self):
		# todo:
		# take the first command and reply with the last answer
		self.parse_ihmcmd(brass_interface.getcommand())
		brass_interface.setresp(self.fill_resp())
		return

	def ihmListInputFile(self):
		self.listFile = os.listdir(os.path.join(os.getcwd(), "recettes"))
		return


	@staticmethod
	def compress_bit_table(data):
		compress = []
		ll = len(data) / 32
		reste = len(data) % 32
		for ii in range(0, ll):
			sm = 0
			for jj in range(0, 32):
				sm += data[ii * 32 + jj] << jj
			compress += [sm]
		sm = 0
		for jj in range(0, reste):
			sm += data[ll * 32 + jj] << jj
		compress += [sm]
		return compress

	def fill_resp(self):
		# ret = json.dumps({'nbcycle': self.nbcycle}) + json.dumps({'timer': self.timer}) + json.dumps({'r_temper': self.r_temper}) + json.dumps({'r_SV': self.r_SV}) + json.dumps({'r_vol': self.r_vol}) + json.dumps({'r_vol_brass': self.r_vol_brass}) + json.dumps({'r_ev': self.r_ev}) + json.dumps({'r_cuveau_pump': self.r_cuveau_pump}) + json.dumps({'r_reverdoir_pump': self.r_reverdoir_pump}) + json.dumps({'r_mixer': self.r_mixer}) + json.dumps({'r_alarm': self.r_alarm)
		# ret = json.dumps({'nbcycle': self.nbcycle, 'timer': self.timer, 'r_temper': self.r_temper, 'r_SV': self.r_SV, 'r_vol': self.r_vol, 'r_vol_brass': self.r_vol_brass, 'r_ev': self.r_ev, 'r_cuveau_pump': self.r_cuveau_pump, 'r_reverdoir_pump': self.r_reverdoir_pump, 'r_mixer': self.r_mixer, 'r_alarm': self.r_alarm})

		# remplir l'état de la brasserie!!
		# FORMAT:
		# 0  1 pour 0 (le tableau va de 1 a 111)
		# 1   11 	(cuveau b) (vide b10%...b100%
		# 12    11 +10	( cuvebrass b +o) vide b10%...b100% o10%..o100%
		# 33    11 + 10 (cuvebu b+ o)vide b10%...b100% o10%..o100%
		# 54    6	(reverdoir b) vide b20%..b100%
		# 60    22   	(t: b- v / b - v / b - v / b - v / b - v - o / b - v - o / b - v - o / b - v - o / b - v /
		# 82    16    (ev: b - cl / b - cl / b - cl - o / b - cl - o / b - cl - o / b - cl - o / )
		# 98    8	(m: off/ on x4) mel / p recircul / p reverdoir / p"mixer" en cleaning
		# 106   6	(r: off/ on x3) cuveau / -- / rever / cuvebu
		#
		# ex:
		# [0,
		#  (1) 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
		#  (12)1,
		#  (13)0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		#  (23)0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
		#  (33)1,
		#  (34)0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		#  (44)0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
		#  (54)1, 0, 0, 0, 0, 1,
		#  (60)0, 1, 0, 1, 1, 0, 1, 0,
		#  (68)0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0,
		#  (82)0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0,
		#  (98)1, 0, 0, 1, 0, 1, 0, 0,
		# (106)0, 1, 1, 0, 0, 1]
		ret = [0] * 112

		ret[1] = 1  # empty cuveau
		ret[1 + self.r_vol[0] * 10 / 75] = 1  # todo mettre la formule exacte !!

		ret[12] = 1  # empty cuvebrass
		tmp = self.r_vol_brass * 10 / 75   # todo mettre la formule exacte !!
		if tmp > 0:
			if self.cleaning_process:
				ret[12 + tmp] = 1    # bleu
			else:
				ret[22 + tmp] = 1    # orange

		ret[33] = 1  # empty cuvebu
		tmp = self.r_vol[2] * 10 / 75   # todo mettre la formule exacte !!
		if tmp > 0:
			if self.cleaning_process:
				ret[33 + tmp] = 1  # bleu
			else:
				ret[43 + tmp] = 1  # orange

		ret[54] = 1  # empty reverdoir
		ret[54 + self.r_vol[1] * 5 / 10] = 1  # todo mettre la formule exacte !!

		ret[60] = 1     # todo zut on fait comment??? pour tuyau 1?
		#  ret[61] = 1  # todo zut on fait comment???  pour tuyau 1?
		if self.r_ev[0]:    # vanne 1 bleu (82) + tuyau 2 bleu(62)
			ret[62] = 1
			ret[82] = 1
		else:               # vanne 1 fermé(83) + tuyau 2 vide(63)
			ret[63] = 1
			ret[83] = 1
		if self.r_ev[1]:    # vanne 2 bleu (84) + tuyau 4 bleu (66)
			ret[66] = 1
			ret[84] = 1
		else:               # vanne 2 fermé(85) + tuyau 4 vide (67)
			ret[67] = 1
			ret[85] = 1
		if self.r_ev[2]:    # vanne 3 bleu(86) ou orange (88) + tuyau 5 bleu (68) ou orange (69)
			if self.cleaning_process:
				ret[68] = 1
				ret[86] = 1
			else:
				ret[69] = 1
				ret[88] = 1
		else:               # vanne 3 fermé (87) + tuyau 5 vide (70)
			ret[70] = 1
			ret[87] = 1
		if self.r_ev[3]:    # vanne 4 bleu (89) ou orange (91) + tuyau 6 bleu (71) ou orange (72)
			if self.cleaning_process:
				ret[71] = 1
				ret[89] = 1
			else:
				ret[72] = 1
				ret[91] = 1
		else:               # vanne 4 fermé (90) + tuyau 6 vide (73)
			ret[73] = 1
			ret[90] = 1

		if self.r_ev[4]:    # vanne 5 blzue(92) ou orange (94)+ tuyau 7 bleu (74) ou orange (75)
			if self.cleaning_process:
				ret[74] = 1
				ret[92] = 1
			else:
				ret[75] = 1
				ret[94] = 1
		else:               # vanne 5 ferm& (93) + tuyau 7 vide (76)
			ret[76] = 1
			ret[93] = 1

		if self.r_ev[5]:   # vanne 6 bleue(95) ou orange (97) + tuyau 9 bleu (80) ou tuyau 8 orange (78)
			# TODO: quand pour le tuyau 8 bleue!! =77 quand on vide arghhh non il faut refaire un truc pour ca pour mettre la pompe!!!!!
			if self.cleaning_process:
				ret[80] = 1
				ret[95] = 1
			else:
				ret[78] = 1
				ret[97] = 1
		else:               # vanne 6 fermé(96) + tuyau 8 vide (79) ou tuyau 9 vide (81)
			ret[96] = 1
			if self.cleaning_process:
				ret[81] = 1
			else:
				ret[79] = 1

		if self.r_mixer == 1:     # mixer ou pump de cleaning OFF
			if self.cleaning_process:
				ret[104] = 1
			else:
				ret[98] = 1
		else:
			if self.cleaning_process:
				ret[105] = 1
			else:
				ret[99] = 1
		if self.r_cuveau_pump == 1:
			ret[65] = 1   # tuayu 3 vide
			ret[100] = 1
		else:
			ret[64] = 1   # tuyau 3 bleu
			ret[101] = 1
		if self.r_reverdoir_pump == 1:
			ret[102] = 1
		else:
			ret[103] = 1

		if self.r_SV[0] == 0:
			ret[106] = 1
		else:
			ret[107] = 1
		if self.r_SV[2] == 0:
			ret[108] = 1
		else:
			ret[109] = 1
		if self.r_SV[3] == 0:
			ret[110] = 1
		else:
			ret[111] = 1

		ret = self.compress_bit_table(ret)
		# format: 111 bits => 4 int
		# after add the other informations to this list

		ret += self.r_temper + self.r_SV + self.r_vol + [self.r_vol_brass] + [self.timer, self.timer - self.begin_time, self.nbcycle]

		if  self.r_alarm == 0:  #  ALARM ON!! attention c'est inversé...
			ret += [1] + [self.r_alarm_txt]
		else:
			ret += [0] + [""]
		ret += [self.listFile, self.inputfileContent1, self.inputfileContent2]

		# manque:
		# TODO CONSOLE: ???? ca va etre compliqué....
		#
		# fichier
		# TODO  config???
		# TODO data ???

		return ret

	def isrestart(self, r):
		self.restart = r
		return

	def quit(self):
		#TODO!!!! tout arreter proprement + quitter!!!
		self.isQuit = True
		return

	def setinputfile(self, file):
		self.inputfile = open(os.path.join(os.getcwd(), "recettes", os.path.basename(file)), 'r')   #  .ibf nput brewerie file, oui c'est naze...
		self.listFile = ""  # plus besoin d'envoyer cela une fois le fichier selectionné
		self.inputfileContent1 = self.inputfile.readline()
		self.inputfileContent2 = self.inputfile.readline()
		return


	def parse_ihmcmd(self, cmd):
		#cmd is a dictionnary! and an have any cmd!
		if not cmd:
			return []
		if "CUVEAU_FILL" in cmd: self.cuveau_fill(cmd.get("CUVEAU_FILL"))
		if "CUVEAU_HEAT" in cmd: self.cuveau_heat(cmd.get("CUVEAU_HEAT"))
		if "CUVEBRASS_FILL" in cmd: self.cuvebrass_fill(cmd.get("CUVEBRASS_FILL"))
		if "REVERDOIR_HEAT" in cmd: self.reverdoir_heat(cmd.get("REVERDOIR_HEAT"))
		if "CUVEBRASS_EMPTY" in cmd: self.cuvebrass_empty(cmd.get("CUVEBRASS_EMPTY"))
		if "CUVEBU_HEAT" in cmd: self.cuvebu_heat(cmd.get("CUVEBU_HEAT"))
		if "CUVEBU_EMPTY" in cmd: self.cuvebu_empty(cmd.get("CUVEBU_EMPTY"))
		if "REVERDOIR" in cmd: self.reverdoir_recircul(cmd.get("REVERDOIR"))
		if "PUMPRECIRCULEAU" in cmd: self.cuveau_recircul(cmd.get("PUMPRECIRCULEAU"))
		if "MIXER" in cmd: self.mixer_onoff(cmd.get("MIXER"))
		if "ALARM" in cmd: self.alarm_onoff(True, cmd.get("ALARM"))
		if "PUMP_EMPTY_CUVEBU" in cmd: self.pump_empty_cuvebu()
		if "EMMERGENCY_STOP" in cmd: self.alarm_onoff(True, "TODO: CRITICAL ALARM: EMERGENCY STOP!!!!!") #TODO il faut aussi arreter!!!
		if "TEST" in cmd: self.autotest()
		if "TEST_ALL" in cmd: self.autotestempty()
		if "PAUSE" in cmd: self.pauseonoff(cmd.get("PAUSE"))
		if "RESTART" in cmd: self.isrestart(cmd.get("RESTART"))
		if "QUIT" in cmd: self.quit()
		if "SELECT_INPUT_FILE" in cmd: self.setinputfile(cmd.get("SELECT_INPUT_FILE"))
		return

	def cycle(self):

		#time of the cycle
		self.timer = int(time.time())
		self.nbcycle += 1

		self.order()
		if not self.cleaning_process:
			self.cycle_cuveau()
			self.cycle_brass_rever()
			self.cycle_ebu()
		else:
			self.cycle_cleaning()

		tmp_vol_cuveau = self.r_vol[0]
		tmp_vol_cuvebu = self.r_vol[2]
		#take the measurements
		self.getAllData()
		#update the volume of cuve brass, this volume can increase if isCuveauVidage and decrease if isCuvebuRemplissage
		# self.r_vol_brass = self.r_vol_brass + (tmp_vol_cuveau - self.r_vol[0]) if self.isCuveauVidage else 0 - (self.r_vol[2] - tmp_vol_cuvebu) if self.isCuvebuRemplissage else 0
		if self.isCuveauVidage:
			self.r_vol_brass += tmp_vol_cuveau - self.r_vol[0]
		if self.isCuvebuRemplissage:
			self.r_vol_brass -= self.r_vol[2] - tmp_vol_cuvebu

		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : volume cuve brass = " + str(self.r_vol_brass) + "l"
		#record the measurements
		self.reccord()
		self.ihm()
		while self.pause:
			time.sleep(.200)
			self.ihm()
			pass

		#cuveau
		#if not self.cleaning_process:
		#	self.cycle_cuveau()
		#	self.cycle_brass_rever()
		#	self.cycle_ebu()
		#else:
		#	self.cycle_cleaning()
		#order!!
		#  self.order()
		return

	def quit_brass(self):
		return self.isQuit;
