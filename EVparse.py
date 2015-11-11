import matplotlib.pyplot as plt 
import CANMessage
import sys

in_filename = sys.argv[1]
#out_filename = sys.argv[3]
#hexID = sys.argv[1]

print "Input file name: %s" % in_filename
#print "Output file name: %s" % out_filename
#print "Arbitration ID selected (HEX): %s" % hexID


fread = open(in_filename,'r')
#fwrite = open(out_filename,'w')

whole_file = fread.readlines()
data_lines = whole_file[6:] #skip first 6 lines
i = 0
j = 0
time = []
B7 = []
B6 = []
B5 = [] 
B4 = []
B3 = []
B2 = []
B1 = []
B0 = []
Bnew = []

messages = [CANMessage.Message()]

indexes = [0,1,2,6,7,8,9,10,11,12,13,16,19,22] #indexes for important CAN data

for each_line in data_lines:
	dat = data_lines[i].split()
	if dat[0] != "End":
		if dat[3] == "Rx":
			newdat = [dat[x] for x in indexes]
			#fwrite.write(str(newdat))
			#fwrite.write('\n')
			temp = CANMessage.Message()
			temp.importMessage(newdat)
			messages.append(temp)
			j = j + 1

	i = i + 1	

brakeMessages = [CANMessage.Message()]
speedMessages = [CANMessage.Message()]
acceleratorPositionMessages = [CANMessage.Message()]
steeringAngleMessages = [CANMessage.Message()]



for i in messages:
	if i.hexID == 0x7D:
		brakeMessages.append(i)
	if i.hexID == 0x75:
		speedMessages.append(i)
	if i.hexID == 0x204:
		acceleratorPositionMessages.append(i)
	if i.hexID == 0x10:
		steeringAngleMessages.append(i)

speedData = []
brakeData = []
acceleratorPosData = []
steeringAngleData = []
byte7 = []
byte6 = []
abyte1 = []
abyte0 = []
apbyte7 = []
apbyte6 = []
apbyte5 = []
sabyte2 = []
sabyte1 = []
sabyte0 = []

for i in brakeMessages:
	brakeData.append(i.combineBytes(7,6))
	byte7.append(i.data[7])
	byte6.append(i.data[6])

for i in speedMessages:
	speedData.append(i.combineBytes(1,0))
	abyte1.append(i.data[1] & 0xF)
	abyte0.append(i.data[0])

for i in acceleratorPositionMessages:
	#acceleratorPosData.append(i)
	apbyte7.append(i.data[7])
	apbyte6.append(i.data[6])
	apbyte5.append(i.data[5])

for i in steeringAngleMessages:
	steeringAngleData.append(i.combineBytes(1,0))
	sabyte0.append(i.data[0])
	sabyte1.append(i.data[1])


for i in range(len(speedData)):
	speedData[i] &= 0xFFF


for i in range(len(steeringAngleData)):
	steeringAngleData[i] &= 0xFFFF

	
plt.figure(1)
plt.title('Proposed Brake Data')
plt.subplot(211)
plt.plot(brakeData,label='Brake Data')
plt.plot(byte7,label='B7')
plt.plot(byte6,label='B6')
plt.legend()
plt.subplot(212)
plt.plot(byte7,label='B7')
plt.legend()

plt.figure(2)
plt.title('Proposed Speed Data')
plt.plot(speedData,label='Speed Data')
plt.plot(abyte1,label='A1')
plt.plot(abyte0,label='A0')
plt.legend()

plt.figure(3)
plt.title('Proposed Accelerator Position Data')
plt.plot(acceleratorPosData,label='Accelerator Position Data')
plt.plot(apbyte7,label='AP7')
plt.plot(apbyte6,label='AP6')
plt.plot(apbyte5,label='AP5')
plt.legend()

plt.figure(4)
plt.title('Proposed Steering Angle Data')
plt.subplot(311)
plt.plot(steeringAngleData,label='Steering Angle Data')
plt.plot(sabyte1,label='SA1')
plt.plot(sabyte0,label='SA0')
plt.legend()
plt.subplot(312)
plt.plot(sabyte1,label='SA1')
plt.legend()
plt.subplot(313)
plt.plot(sabyte0,label='SA0')
plt.legend()
plt.show()