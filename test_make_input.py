# coding=utf-8
import json
import os


def test_makeInputFile_testpc_pasapas():
	# avec chauffe du reverdoir! => multi palier

	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","test_input.ibf"), 'w+')
	oo.write("only for comment1\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': False}) + "\n")
	oo.write(json.dumps({'TIME': 2, 'CUVEAU_FILL': 70}) + "\n")
	oo.write(json.dumps({'TIME': 4, 'CUVEAU_HEAT': 70, 'REVERDOIR_HEAT': 90}) + "\n")
	oo.write(json.dumps({'TIME': 11, 'CUVEBRASS_FILL': 50}) + "\n")
	oo.write(json.dumps({'TIME': 16, 'REVERDOIR': True, 'MIXER': True}) + "\n")
	oo.write(json.dumps({'TIME': 17, 'REVERDOIR': False, 'REVERDOIR_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 18, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'MIXER': False}) + "\n")
	oo.write(json.dumps({'TIME': 21, 'CUVEBRASS_EMPTY': 60, 'CUVEBU_HEAT': 99}) + "\n")
	oo.write(json.dumps({'TIME': 31, 'ALARM': 'BRASSAGE TERMINE!!!!!', 'CUVEBU_EMPTY': 60, 'CUVEBU_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 35, 'ALARM': 'brassage fini'}) + "\n")

	oo.write(json.dumps({'TIME': 600}) + "\n")


# schedule_pasapas = [[ 1, 20, 20, 20, 20,  0,  0,  0,  0],
# 				[ 2, 20, 20, 20, 20,  0,  0,  0,  0],   # debut, remplissage reverdoir de 7l ("a la main")
# 				[ 3, 20, 20, 20, 20,  0,  7,  0,  0],   # remplissage cuveau à 70l + reverdoir 10L =>
# 				[ 4, 20, 20, 20, 20, 70, 10,  0,  0],   # cuveau remplit 70l chauffe 70 + reverdoir 90
# 				[ 5, 70, 20, 90, 20, 70, 10,  0,  0],   # cuveau a 70, vidage 50l dans cuve brass
# 				[ 6, 70, 65, 90, 20, 20, 10,  0, 50],   # cuvebrass 50l  a 65, reverdoir on, mixer on
# 	            [ 7, 70, 68, 90, 20, 20, 10,  0, 50],   # cuvebrass 50l  a 65, mixer on
# 	            [ 8, 20, 68, 90, 20,  0, 10,  0, 70],   # rincage et arret chauffe cuve eau
# 	            [ 9, 20, 20, 90, 60,  0, 10, 60, 10],   # remplissage cuve ebu
# 	            [ 10, 20, 20, 90, 70,  0, 10, 60, 10],   # ebu
# 	            [11, 20, 20, 90, 98,  0, 10, 60, 10],   # Fin ebu
# 	            [12, 20, 20, 20, 20,  0, 10,  0, 10]]   # Fin brass


def test_makeInputFile_testpc_realtime():
	# avec chauffe du reverdoir! => multi palier

	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","test_input.ibf"), 'w+')
	oo.write("only for comment1\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': False}) + "\n")
	oo.write(json.dumps({'TIME': 2, 'CUVEAU_FILL': 70}) + "\n")
	oo.write(json.dumps({'TIME': 4, 'CUVEAU_HEAT': 70, 'REVERDOIR_HEAT': 90}) + "\n")
	oo.write(json.dumps({'TIME': 11, 'CUVEBRASS_FILL': 50}) + "\n")
	oo.write(json.dumps({'TIME': 16, 'REVERDOIR': True, 'MIXER': True}) + "\n")
	oo.write(json.dumps({'TIME': 20, 'REVERDOIR': False, 'REVERDOIR_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 24, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'MIXER': False}) + "\n")
	oo.write(json.dumps({'TIME': 26, 'CUVEBRASS_EMPTY': 60, 'CUVEBU_HEAT': 99}) + "\n")
	oo.write(json.dumps({'TIME': 42, 'ALARM': 'BRASSAGE TERMINE!!!!!', 'CUVEBU_EMPTY': 60, 'CUVEBU_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 47, 'ALARM': 'brassage fini'}) + "\n")

def test_makeInputFile_testpc_realtime_long():
	# avec chauffe du reverdoir! => multi palier

	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","test_input.ibf"), 'w+')
	oo.write("only for comment1\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': False}) + "\n")
	oo.write(json.dumps({'TIME': 20, 'CUVEAU_FILL': 70}) + "\n")
	oo.write(json.dumps({'TIME': 40, 'CUVEAU_HEAT': 70, 'REVERDOIR_HEAT': 90}) + "\n")
	oo.write(json.dumps({'TIME': 110, 'CUVEBRASS_FILL': 50}) + "\n")
	oo.write(json.dumps({'TIME': 160, 'REVERDOIR': True, 'MIXER': True}) + "\n")
	oo.write(json.dumps({'TIME': 200, 'REVERDOIR': False, 'REVERDOIR_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 240, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'MIXER': False}) + "\n")
	oo.write(json.dumps({'TIME': 260, 'CUVEBRASS_EMPTY': 60, 'CUVEBU_HEAT': 99}) + "\n")
	oo.write(json.dumps({'TIME': 420, 'ALARM': 'BRASSAGE TERMINE!!!!!', 'CUVEBU_EMPTY': 60, 'CUVEBU_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 470, 'ALARM': 'brassage fini'}) + "\n")


def test_makeInputFile():
	# sans chauffe du reverdoir!

	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	print(os.path.join("recettes", "test_input.ibf"))
	oo = open(os.path.join("recettes","test_input.ibf"), 'w+')
	oo.write("only for comment1\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': False}) + "\n")
	oo.write(json.dumps({'TIME': 0, 'CUVEAU_FILL': 70, 'CUVEAU_HEAT': 68}) + "\n")
	oo.write(json.dumps({'TIME': 30, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 75}) + "\n")
	oo.write(json.dumps({'TIME': 40, 'CUVEBRASS_FILL': 30, 'MIXER': True}) + "\n")
	oo.write(json.dumps({'TIME': 45, 'CUVEAU_FILL': 20, 'CUVEAU_HEAT': 80}) + "\n")
	oo.write(json.dumps({'TIME': 45, 'REVERDOIR': True, 'MIXER': False}) + "\n")
	oo.write(json.dumps({'TIME': 95, 'CUVEAU_HEAT': 0, 'CUVEBRASS_FILL': 10}) + "\n")
	oo.write(json.dumps({'TIME': 100, 'REVERDOIR': False, 'CUVEBRASS_EMPTY': 20}) + "\n")
	oo.write(json.dumps({'TIME': 105, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'CUVEBU_HEAT': 99}) + "\n")
	oo.write(json.dumps({'TIME': 115, 'CUVEBRASS_EMPTY': 50}) + "\n")
	oo.write(json.dumps({'TIME': 130, 'ALARM': 'houblon amérisant'}) + "\n")
	oo.write(json.dumps({'TIME': 190, 'ALARM': 'houblon aromatique'}) + "\n")
	oo.write(json.dumps({'TIME': 195, 'ALARM': 'BRASSAGE TERMINE!!!!!'}) + "\n")
	oo.write(json.dumps({'TIME': 600}) + "\n")


def test_makeInputFile_multi():
	# avec chauffe du reverdoir! => multi palier

	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","test_input.ibf"), 'w+')
	oo.write("only for comment1\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': False}) + "\n")
	oo.write(json.dumps({'TIME': 0, 'CUVEAU_FILL': 70, 'CUVEAU_HEAT': 68}) + "\n")
	oo.write(json.dumps({'TIME': 30, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 75, 'REVERDOIR_HEAT': 95}) + "\n")
	oo.write(json.dumps({'TIME': 40, 'CUVEBRASS_FILL': 30, 'MIXER': True}) + "\n")
	oo.write(json.dumps({'TIME': 45, 'CUVEAU_FILL': 20, 'CUVEAU_HEAT': 80}) + "\n")
	oo.write(json.dumps({'TIME': 45, 'REVERDOIR': True, 'MIXER': False}) + "\n")
	oo.write(json.dumps({'TIME': 95, 'CUVEAU_HEAT': 0, 'CUVEBRASS_FILL': 10}) + "\n")
	oo.write(json.dumps({'TIME': 100, 'REVERDOIR': False, 'CUVEBRASS_EMPTY': 20, 'REVERDOIR_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 105, 'CUVEBRASS_FILL': 20, 'CUVEAU_HEAT': 0, 'CUVEBU_HEAT': 99}) + "\n")
	oo.write(json.dumps({'TIME': 115, 'CUVEBRASS_EMPTY': 50}) + "\n")
	oo.write(json.dumps({'TIME': 130, 'ALARM': 'houblon amérisant'}) + "\n")
	oo.write(json.dumps({'TIME': 190, 'ALARM': 'houblon amérisant'}) + "\n")
	oo.write(json.dumps({'TIME': 195, 'ALARM': 'BRASSAGE TERMINE!!!!!'}) + "\n")
	oo.write(json.dumps({'TIME': 600}) + "\n")


def test_makeInputFile_rincage():
	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","test_input.ibf"), 'w+')
	oo.write("First line for comment... name of the receipt etc...   here is the rincage automated... during the cooling of the batch, the aim is that nothing pour out\n")

	oo.write(json.dumps({'TIME': 600}) + "\n")
	return


def test_makeInputFile_peracetique():
	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","est_peracetique_cleaning.ibf"), 'w+')
	oo.write("Clean the brewerie with peracetique acid in the CUVEEBU, wait then pump it to the CUVEAU, then in the CUVE brass + Reverdoir then un cuveau then in evier...\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': True}) + "\n")
	oo.write(json.dumps({'TIME': 0}) + "\n")
	oo.write(json.dumps({'TIME': 20, 'PUMP_EMPTY_CUVEBU': True}) + "\n")
	oo.write(json.dumps({'TIME': 40, 'CUVEBRASS_FILL': 70}) + "\n")
	oo.write(json.dumps({'TIME': 50, 'REVERDOIR': True}) + "\n")
	oo.write(json.dumps({'TIME': 58, 'REVERDOIR': False}) + "\n")
	oo.write(json.dumps({'TIME': 60, 'CUVEBRASS_EMPTY': 70}) + "\n")
	oo.write(json.dumps({'TIME': 60, 'ALARM': 'NETTOYAGE ACIDE TERMINE branch the evacuation!!'}) + "\n")
	oo.write(json.dumps({'TIME': 62, 'PUMP_EMPTY_CUVEBU': True}) + "\n")
	oo.write(json.dumps({'TIME': 600}) + "\n")
	return


def test_makeInputFile_soude():
	# CUVEAU_FILL
	# CUVEAU_HEAT
	# CUVEBRASS_FILL
	# CUVEBRASS_EMPTY
	# REVERDOIR_HEAT
	# CUVEBU_HEAT
	# CUVEBU_EMPTY
	# REVERDOIR
	# MIXER
	# ALARM
	oo = open(os.path.join("recettes","est_peracetique_cleaning.ibf"), 'w+')
	oo.write("Clean the brewerie with peracetique soude in the CUVEEBU, wait then pump it to the CUVEAU, then in the CUVE brass + Reverdoir then un cuveau then in evier...\n")
	oo.write("only for comment2\n")
	oo.write(json.dumps({'CLEANING_PROCESS': True}) + "\n")
	oo.write(json.dumps({'TIME': 0, 'CUVEBU_HEAT': 80}) + "\n")
	oo.write(json.dumps({'TIME': 20, 'PUMP_EMPTY_CUVEBU': True, 'CUVEAU_HEAT': 80}) + "\n")
	oo.write(json.dumps({'TIME': 40, 'CUVEBRASS_FILL': 70, 'CUVEAU_HEAT': 0}) + "\n")
	oo.write(json.dumps({'TIME': 50, 'REVERDOIR': True}) + "\n")
	oo.write(json.dumps({'TIME': 58, 'REVERDOIR': False}) + "\n")
	oo.write(json.dumps({'TIME': 60, 'CUVEBRASS_EMPTY': 70}) + "\n")
	oo.write(json.dumps({'TIME': 60, 'ALARM': 'NETTOYAGE ACIDE TERMINE branch the evacuation!!'}) + "\n")
	oo.write(json.dumps({'TIME': 62, 'PUMP_EMPTY_CUVEBU': True}) + "\n")
	oo.write(json.dumps({'TIME': 600}) + "\n")
	return


test_makeInputFile()
#test_makeInputFile_testpc_realtime()
#test_makeInputFile_testpc_pasapas()
