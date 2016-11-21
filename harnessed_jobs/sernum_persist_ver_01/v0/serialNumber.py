from org.lsst.ccs.scripting import *

rafts = CCS.attachSubsystem("ccs-reb4")
reb0 = CCS.attachSubsystem("ccs-reb4/REB0")
result = reb0.synchCommandLine(10, "getSerialNumber")

output = open(tsCWD + '/serial_number.txt', 'w')
output.write('%s\n' % result.getResult())
output.close()
