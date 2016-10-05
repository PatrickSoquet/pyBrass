# coding=utf-8
# pour faire fonctionner modbusTCP sous windows:
# télécharger et installer pyModbbusTCP + win_inet_pton
# https://github.com/sourceperl/pyModbusTCP
# https://pypi.python.org/pypi/win_inet_pton


import brass_PID
import win_inet_pton
import socket

pd = brass_PID.pid()
#pd.init_all_pid()
# pd.read_all_temp_SV()

# essai sur les rampes!!!!
# si temp est de 20°

#pd.init_all_pid()
# pd.write_SV(0,220)
print pd.read_all_temp_SV()
# pd.pids[0].write_single_register(16,0)
#print pd.pids[0].read_holding_registers(0x0B,4)
#aa = pd._read_all(0)
#print pd._read_all(1)
#print aa

#pd.write_SV(1,178)

# SV = PV+5° => chauffe tt le tps

