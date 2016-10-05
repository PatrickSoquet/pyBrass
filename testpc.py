# coding=utf-8
#  to write a scenario to test the whole SW chain on PC!
import brass_process


# brass_proc = brass_process.brasserie
# schedule: tableau n*m, n etapes, m param (tobe determined)
# liste des paramètres:
# 0: timer
# 1: r_temper_cuvebu_0
# 2: r_temp_cuve_brass_1
# 3: r_temp_cuve_reverdoir_2
# 4: r_temp_cuve_ebu_3
# self.r_temper = [0] * 4  # cuveau / cuve brass / reverdoir / cuvebu
# useless: self.r_SV = [0] * 4  # cuveau / cuve brass(non util) / reverdoir / cuvebu
# 5: r_vol_cuveau_0
# 6: r_vol_rev_1
# 7: r_vol_cuvebu_2
# self.r_vol = [0] * 3  # cuveau / reverdoir / cuvebu
# 8: r_vol_brass
# self.r_vol_brass = 0  # calculated!!


#_TEST_PASAPAS = brass_process._TEST_PASAPAS


class testpc:
	"""
	@type brass_proc: brass_process.brasserie
	"""
	liste = {"r_temper_cuveau_0": 1, "r_temper_cuve_brass_1": 2, "r_temper_cuve_reverdoir_2": 3, "r_temper_cuvebu_3": 4, "r_vol_cuveau_0": 5, "r_vol_rev_1": 6, "r_vol_cuvebu_2": 7, "r_vol_brass": 8}
	#                        |  temp       |v eau rev ebu brass
	#                     0   1   2   3   4   5   6   7   8
	schedule_pasapas = [[ 1, 20, 20, 20, 20,  0,  0,  0,  0],
					    [ 2, 20, 20, 20, 20,  0, 10,  0,  0],   # debut, remplissage reverdoir de 10l ("a la main") + 'CUVEAU_FILL': 70
						[ 3, 20, 20, 20, 20, 10, 10,  0,  0],
						[ 4, 20, 20, 20, 20, 20, 10,  0,  0],   # CUVEAU_HEAT': 70, 'REVERDOIR_HEAT': 90
						[ 5, 35, 20, 60, 20, 30, 10,  0,  0],
						[ 6, 45, 20, 88, 20, 40, 10,  0,  0],
						[ 7, 55, 20, 92, 20, 50, 10,  0,  0],
						[ 8, 65, 20, 88, 20, 60, 10,  0,  0],
						[ 9, 68, 20, 90, 20, 70, 10,  0,  0],   # cuveau remplit 70l
						[10, 70, 20, 90, 20, 70, 10,  0,  0],   # cuveau à 70°
					    [11, 70, 20, 90, 20, 70, 10,  0,  0],   # 'CUVEBRASS_FILL': 50
					    [12, 70, 25, 90, 20, 60, 10,  0, 10],
					    [13, 70, 30, 90, 20, 50, 10,  0, 20],
					    [14, 70, 45, 90, 20, 40, 10,  0, 30],
					    [15, 70, 55, 90, 20, 30, 10,  0, 40],
					    [16, 70, 65, 90, 20, 20, 10,  0, 50],      # cuvebrass 50l  a 65°, 'REVERDOIR': True, 'MIXER': True
		                [17, 70, 68, 90, 20, 20, 10,  0, 50],   # cuvebrass  68°  'REVERDOIR': False, 'REVERDOIR_HEAT':0
		                [18, 70, 68, 90, 20, 20, 10,  0, 50],  # 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'MIXER': False
		                [19, 70, 68, 90, 20, 10, 10,  0, 60],
		                [20, 70, 68, 90, 20,  0, 10,  0, 70], #rincage finit
		                [21, 70, 68, 90, 20,  0, 10,  0, 70],   #'CUVEBRASS_EMPTY': 60, 'CUVEBU_HEAT': 99
		                [22, 70, 68, 90, 50, 0, 10, 10, 60], # nothing... oublie
	                    [23, 70, 68, 90, 50,  0, 10, 10, 60],
		                [24, 70, 68, 90, 50,  0, 10, 20, 50],
		                [25, 70, 68, 90, 60,  0, 10, 30, 40],
		                [26, 70, 68, 90, 65,  0, 10, 40, 30],
		                [27, 70, 68, 90, 70,  0, 10, 50, 20],
		                [28, 70, 68, 90, 80,  0, 10, 60, 10],  # cuvebu à 60l
		                [29, 70, 68, 90, 95,  0, 10, 60, 10],  # cuvebu à 60l
		                [30, 70, 68, 90, 100, 0, 10, 55, 10],  # cuvebu à 100°, le volume a réduit a 55!
		                [31, 70, 68, 90, 100, 0, 10, 55, 10], # 'ALARM': 'BRASSAGE TERMINE!!!!!', 'CUVEBU_EMPTY': 60, 'CUVEBU_HEAT': 0})
		                [32, 70, 68, 90, 100, 0, 10, 40, 10],
		                [33, 70, 68, 90, 100, 0, 10, 20, 10],
		                [34, 70, 68, 90, 100, 0, 10, 10, 10],
		                [35, 70, 68, 90, 100, 0, 10,  0, 10]] # Fin brass


	schedule_realtime = [[ 1, 20, 20, 20, 20,  0,  0,  0,  0],
					    [ 2, 20, 20, 20, 20,  0, 10,  0,  0],   # debut, remplissage reverdoir de 10l ("a la main") + 'CUVEAU_FILL': 70
						[ 3, 20, 20, 20, 20, 10, 10,  0,  0],
						[ 4, 20, 20, 20, 20, 20, 10,  0,  0],   # CUVEAU_HEAT': 70, 'REVERDOIR_HEAT': 90
						[ 5, 35, 20, 60, 20, 30, 10,  0,  0],
						[ 6, 45, 20, 88, 20, 40, 10,  0,  0],
						[ 7, 55, 20, 92, 20, 50, 10,  0,  0],
						[ 8, 65, 20, 88, 20, 60, 10,  0,  0],
						[ 9, 68, 20, 90, 20, 70, 10,  0,  0],   # cuveau remplit 70l
						[10, 70, 20, 90, 20, 70, 10,  0,  0],   # cuveau à 70°
					    [11, 70, 20, 90, 20, 70, 10,  0,  0],   # 'CUVEBRASS_FILL': 50
					    [12, 70, 25, 90, 20, 60, 10,  0, 10],
					    [13, 70, 30, 90, 20, 50, 10,  0, 20],
					    [14, 70, 45, 90, 20, 40, 10,  0, 30],
					    [15, 70, 55, 90, 20, 30, 10,  0, 40],
					    [16, 70, 65, 90, 20, 20, 10,  0, 50],      # cuvebrass 50l  a 65°, 'REVERDOIR': True, 'MIXER': True
		                [20, 70, 68, 90, 20, 20, 10,  0, 50],   # cuvebrass  68°  'REVERDOIR': False, 'REVERDOIR_HEAT':0
		                [24, 70, 68, 90, 20, 20, 10,  0, 50],  # 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'MIXER': False
		                [25, 70, 68, 90, 20, 10, 10,  0, 60],
		                [24, 70, 68, 90, 20,  0, 10,  0, 70], #rincage finit
		                [26, 70, 68, 90, 20,  0, 10,  0, 70],   #'CUVEBRASS_EMPTY': 60, 'CUVEBU_HEAT': 99
		                [27, 70, 68, 90, 50,  0, 10, 10, 60],
		                [28, 70, 68, 90, 50,  0, 10, 20, 50],
		                [29, 70, 68, 90, 60,  0, 10, 30, 40],
		                [30, 70, 68, 90, 65,  0, 10, 40, 30],
		                [31, 70, 68, 90, 70,  0, 10, 50, 20],
		                [32, 70, 68, 90, 80,  0, 10, 60, 10],  # cuvebu à 60l
		                [35, 70, 68, 90, 95,  0, 10, 60, 10],  # cuvebu à 60l
		                [40, 70, 68, 90, 100, 0, 10, 55, 10],  # cuvebu à 100°, le volume a réduit a 55!
		                [42, 70, 68, 90, 100, 0, 10, 55, 10], # 'ALARM': 'BRASSAGE TERMINE!!!!!', 'CUVEBU_EMPTY': 60, 'CUVEBU_HEAT': 0})
		                [43, 70, 68, 90, 100, 0, 10, 40, 10],
		                [44, 70, 68, 90, 100, 0, 10, 20, 10],
		                [45, 70, 68, 90, 100, 0, 10, 10, 10],
		                [46, 70, 68, 90, 100, 0, 10,  0, 10],
		                [47, 70, 68, 90, 100, 0, 10,  0, 10]] # Fin brass




	timer_max = 34
	timer_i = 0
	brass_proc = None

	@staticmethod
	def init_static(bp):
		"""
		@type bp: brass_process.brasserie
		"""
		global brass_proc
		brass_proc = bp
		global timer_i
		timer_i = 0
		return

	@staticmethod
	def getdata():
		global timer_i
		if brass_process._TEST_PASAPAS:
			if brass_proc.nbcycle > testpc.schedule_pasapas[timer_i][0] and timer_i < testpc.timer_max:
				timer_i += 1
			print str(timer_i)
			# return testpc.schedule_pasapas[timer_i][testpc.liste[param]]
			return testpc.schedule_pasapas[timer_i]
		else:
			if (brass_proc.timer - brass_proc.begin_time) > testpc.schedule_realtime[timer_i][0] and timer_i < testpc.timer_max:
				timer_i += 1
			print str(timer_i)
			# return testpc.schedule_realtime[timer_i][testpc.liste[param]]
			return testpc.schedule_realtime[timer_i]

