import machine
from machine import Pin, UART
from machine import Pin
#from microdot import Microdot
import time
import sys
import network
import socket

p21 = Pin(21, Pin.IN)
p22 = Pin(22, Pin.IN)
sdaPIN=machine.Pin(4)
sclPIN=machine.Pin(5)

buf = bytearray(1)
buf_3 = bytearray(3)
buf_8 = bytearray(9)
Read_Data = bytearray(6)
i2c_Data_In = bytearray(2)
i2C_Data_Out = bytearray(2)

K3_Band_MR_ML = 0
K3_Band_R_L = 0
VB_Band = 0
Multi = 0
L_R = 0
J46_U23 = 0
J47_U20 = 0
J47_U24 = 0
J45_U26 = 0
J46_U21 = 0
J48_U29_P1 = 0

Use_Wifi = 0

Band_10	=		9
Band_15	=		7
Band_20	=		5
Band_40	=		3
Band_80	=		2
Band_160 =		1
Band_None	=	15

BPF_10	=		1
BPF_15	=		2
BPF_20	=		4
BPF_40	=		8
BPF_80	=		16
BPF_160	=		32

#'****************************************************************************
#'
#'	J45_Even
#'
#'		U28 (Inputs)
#'
#'			P00 (LSB)  		Spare 4 Tip	
#'			P01			Spare 4 Ring
#'			P02			Spare 5 Tip
#'			P03			Spare_5 Ring
#'			P04			Foot Switch Ring	Spare
#'			P05			PTT Winkeyer Left	(High)
#'			P06			PTT Winkeyer Right(High)
#'			P07			Foot Switch	Tip	(Low)
#'
#'			P10			Unused
#'			P11			Unused
#'			P12			Unused
#'			P13			Unused
#'			P14			Unused
#'			P15			Unused
#			P16			Unused
#'			P17			Unused
#'
#'	J45 Odd
#'
#'		U26 (Outputs)
#'
#'			P00 (LSB)		Unused
#'			P01			Unused
#'			P02			Unused
#'			P03			Unused
#'			P04			Unused
#'			P05			Unused
#'			P06			Unused
#'			P07			Unused
#'
#			P10			Spare 6 Tip 	(Low)		- Amp L Power On  AMP_PWR
#'			P11			Spare 6 Ring 	(Low)		- Amp R Power On	AMP_PWR
#'			P12			Spare 7 Tip 	(Low)		- ACOM PWR ON Pulse L
#'			P13			Spare 7 Ring 	(Low)		- ACOM PWR ON Pulse R
#'			P14			Spare 8 Tip 	(Low)		- Amp Sel L		Dupe of Amp_Sel
#'			P15			Spare 8 Ring 	(Low)		- Amp Sel R
#'			P16			Spare 9 Tip 	(Low)		- Bev Direction temp HI (low)
#'			P17			Spare 9 Ring 	(Low)		- Bev Direction temp LO (low)
#'
#
#'	J46_Even
#'
#'		U23 (Outputs)
#'
#'			P00 (LSB)  		Bev Select ML	(High)
#'			P01			Bev Select MR	(High)
#'			P02			Bev Select L	(High)
#'			P03			Bev Select R	(High)
#'			P04			Amp Relay ML	(Low)
#'			P05			Amp Relay L		(Low)
#'			P06			Amp Relay R		(Low)
#'			P07			Amp Relay MR	(Low)
#'
#'			P10			Spare DB9 - 5
#'			P11			Multi	Op 		(Low)
#'			P12			K3 TX Inhibit R	(High)
#'			P13			K3 TX Inhibit L	(High)
#'			P14			K14 TX Inhibit MR	(High)
#'			P15			K3 TX Inhibit ML	(High)
#'			P16			Remote Mode		(High)
#'			P17			Unused
#'
#'	J46 Odd
#'
#'		U21 (Outputs)
#'
#'			P00 (LSB)		Unused
#'			P01			Unused
#'			P02			Unused
#'			P03			Unused
#'			P04			Left Radio		(Low)
#'			P05			Right Radio		(Low)
#'			P06			Amp Select Left	(Low)
#'			P07			Amp Select Right	(Low)
#'
#'			P10			Spare DB9 - 1
#'			P11			Spare DB9 - 6
#'			P12			Spare DB9 - 2
#'			P13			Spare DB9 - 7
#'			P14			Spare DB9 - 3
#'			P15			Spare DB9 - 8
#'			P16			Spare DB9 - 4
#'			P17			Spare DB9 - 9
#'
#'	J47_Even
#'
#'		U20 (Outputs)
#'
#'			P00 (LSB)  		BPF 10 R		(High)
#'			P01			BPF 15 R		(High)
#'			P02			BPF 20 R		(High)
#'			P03			BPF 40 R		(High)
#			P04			BPF 80 R		(High)
#'			P05			BPF 160 R		(High)
#'			P06			Spare 3 Tip					TX INH L
#'			P07			Spare 3 Ring				TX INH R
#'
#'			P10			BPF 10 MR		(High)
#'			P11			BPF 15 MR		(High)
#'			P12			BPF 20 MR		(High)
#'			P13			BPF 40 MR		(High)
#'			P14			BPF 80 MR		(High)
#'			P15			BPF 160 MR		(High)
#'			P16			Local RX Preamp	(High)
#'			P17			Multi Old		(Low)
#'
#'	J47 Odd
#'
#'		U24 (Outputs)
#'
#'			P00 (LSB)  		BPF 10 ML		(High)
#'			P01			BPF 15 ML		(High)
#'			P02			BPF 20 ML		(High)
#'			P03			BPF 40 ML		(High)
#'			P04			BPF 80 ML		(High)
#'			P05			BPF 160 ML		(High)
#'			P06			RX Direction H	(Low)
#'			P07			RX Direction L	(Low)
#'
#'			P10			BPF 10 L		(High)
#'			P11			BPF 15 L		(High)
#'			P12			BPF 20 L		(High)
#'			P13			BPF 40 L		(High)
#'			P14			BPF 80 L		(High)
#'			P15			BPF 160 L		(High)
#'			P16			Remote Mode		(Low)
#'			P17			Audio Amp Off	(Low)
#'
#'	J48_Even
#'
#'		U29 (P0 - Inputs, P1 -Outputs)
#'
#'			P00 (LSB)  		Wattmeter Alarm ML (Low)
#'			P01			Wattmeter Alarm L  (Low)
#'			P02			Wattmeter Alarm R  (Low)
#'			P03			Wattmeter Alarm MR (Low)
#'			P04			Amp PTT In ML	 (Low)
#'			P05			Amp PTT In L	 (Low)
#'			P06			Amp PTT In R	 (Low)
#'			P07			Amp PTT In MR	 (Low)
#'
#'			P10			K3 Power On L	(High)
#'			P11			K3 Power On R	(High)
#'			P12			K3 Power On ML	(High)
#'			P13			K3 Power On MR	(High)
#'			P14			Spare 1 Tip		Does not work in one MCB
#'			P15			Spare 1 Ring
#'			P16			Spare 2 Tip		Bev Dir Lo  Dupe of SP9
#'			P17			Spare 2 Ring	Bev Dir Lo
#'
#'		U27 (Inputs)
#'
#'			P00 (LSB)  		K3 Band 0 ML	(High)
#'			P01			K3 Band 1 ML	(High)
#'			P02			K3 Band 2 ML	(High)
#'			P03			K3 Band 3 ML	(High)
#'			P04			K3 Band 0 MR	(High)
#'			P05			K3 Band 1 MR	(High)
#'			P06			K3 Band 2 MR	(High)
#'			P07			K3 Band 3 MR	(High)
#'
#'			P10			K3 Band 0 L		(High)
#'			P11			K3 Band 1 L		(High)
#'			P12			K3 Band 2 L		(High)
#'			P13			K3 Band 3 L		(High)
#'			P14			K3 Band 0 R		(High)
#'			P15			K3 Band 1 R		(High)
#'			P16			K3 Band 2 R		(High)
#'			P17			K3 Band 3 R		(High)
#'
#'	Audio Relays
#'
#'		Command 0		Reset (Soft Mode, Switches Open)
#'
#'		Command 192		SwitchSet
#'
#					Byte 0 - XXXXX SW11 SW10 SW9
#'					Byte 1 - SW8 - SW1
#'						
#'	Mode_Bits
#'
#'		Bit 7		L/R
#'		Bit 6		RX Ant Direction Hi
#'		Bit 5		RX Ant Direction Lo
#'
#'	Mode_Bits_1 - MCB_Out(4)
#'	 	
#'	Output
#'		B1
#'		K3_Band_MR_ML
#'		K3_Band_R_L
#'		B0
#'		B3
#'		J46_U23 LO
#'		J46_U21 LO
#'		J47_U24 LO
#'	
#'	Inp_Switches  (SO2R)  (SW_U31 compatible)
#'
#'		bit15 (MSB)	160 Lower position			(High)
#'		bit14		160 Upper position			(High)
#'		bit13		80  Lower position			(High)		
#'		bit12		80  Upper Position			(High)
#'		bit11		40  Lower Position			(High)
#'		bit10	      40  Upper Position			(High)
#'		bit9		SKY selected for radio L		(High)
#'		bit8		C3E selected for radio L		(High)
#'
#'		bit7		SKY selected for radio R		(High)
#'		bit6		C3E selected for radio R		(High)
#'		bit5		Tribanders for radio L			(High)
#'		bit4		10/15/20 Mono for radio L		(High)
#'		bit3		Tribanders for radio R			(High)
#'		bit2		10/15/20 Mono for radio R	 	(High)
#'		bit1		RX Ant L					(Low)		
#'		bit0		RX Ant R					(Low)
#'
#'*****************************************************************************

J47_Even = 33 	# %01000010	 	 U20 - Bus 0
J46_Odd = 34	# %01000100		' U21 - Bus 0
J46_Even = 38	# %01001100		' U23 - Bus 0
J47_Odd = 35	# %01000110		' U24 - Bus 0
J45_Odd = 32	# %01000000		' U26 - Bus 1
J48_Odd = 37	# %01001010		' U27 - Bus 1
J45_Even = 36	# %01001000		' U28 - Bus 1
J48_Even = 39	# %01001110		' U29 - Bus 1
I2C_Hub = 112	# %11100000

Audio_U1 = 52	# %01101000		' Bus 1

uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
uart.init(bits=8, parity=None, stop=1, timeout = 10000)

i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000, timeout=5000)

if Use_Wifi == 1:
    Wifi = network.WLAN(network.WLAN.IF_STA)
    Wifi.config(pm=0x111022)
    #Wifi.ifconfig(('192.168.1.10', '255.255.255.0', '192.168.1.10', '8.8.8.8'))
    Wifi.active(True)
    #print
    if not Wifi.isconnected():
        Wifi.connect('The_Georgens', '9257852025')
        print('Waiting for connection')
        while not Wifi.isconnected():
            time.sleep(1)
    print(Wifi.ipconfig("addr4"))
    print(Wifi.config('ssid'))
    print(Wifi.config('channel'))
    Sockaddr = ('192.168.2.131', 10050)
    print(Sockaddr)
    MCB = socket.socket()
    MCB.settimeout(200)
    try:
        MCB.connect(Sockaddr)
    except:
        print('Socket Connect Failed')
    else:
        print('must have connected')
    #MCB.write('C - this is a test')
    #try:
        #print(MCB.read(6))
    #except:
        #print('TCP timeout')
buf[0] = 3
i2c.writeto(I2C_Hub, b'\x03')
devices = i2c.scan()

i2c.writeto_mem(J45_Even, 4, b'\x00\x00')
#i2c.writeto_mem(J45_Even, 5, '0')
i2c.writeto_mem(J45_Even, 6, b'\xff\xff')
#i2c.writeto_mem(J45_Even, 7, b'\xff')

i2c.writeto_mem(J48_Even, 4, b'\x00\x00')
#i2c.writeto_mem(J48_Even, 5, '0')
i2c.writeto_mem(J48_Even, 6, b'\x00\xff')
#i2c.writeto_mem(J48_Even, 7, '0')

#i2c.writeto_mem(J48_Odd, 4, '0')
#i2c.writeto_mem(J48_Odd, 5, '0')
#i2c.writeto_mem(J48_Odd, 6, b'\xff')
#i2c.writeto_mem(J48_Odd, 7, b'\xff')

i2c.writeto_mem(J48_Odd, 4, b'\x00\x00')
i2c.writeto_mem(J48_Odd, 6, b'\xff\xff')
#

i2c.writeto_mem(J45_Odd, 4, b'\x00\x00')
i2c.writeto_mem(J45_Odd, 6, b'\x00\x00')
#i2c.writeto_mem(J45_Odd, 6, '0')
#i2c.writeto_mem(J45_Odd, 7, '0')

i2c.writeto_mem(J46_Even, 4, b'\x00\x00')
#i2c.writeto_mem(J46_Even, 5, '0')
i2c.writeto_mem(J46_Even, 6, b'\x00\x00')
#i2c.writeto_mem(J46_Even, 7, '0')

i2c.writeto_mem(J46_Odd, 4, b'\x00\x00')
#i2c.writeto_mem(J46_Odd, 5, '0')
i2c.writeto_mem(J46_Odd, 6, b'\x00\x00')
#i2c.writeto_mem(J46_Odd, 7, '0')

i2c.writeto_mem(J47_Even, 4, b'\x00\x00')
#i2c.writeto_mem(J47_Even, 5, '0')
i2c.writeto_mem(J47_Even, 6, b'\x00\x00')
#i2c.writeto_mem(J47_Even, 7, '0')

i2c.writeto_mem(J47_Odd, 4, b'\x00\x00')
#i2c.writeto_mem(J47_Odd, 5, '0')
i2c.writeto_mem(J47_Odd, 6, b'\x00\x00')
#i2c.writeto_mem(J47_Odd, 7, '0')

i2c.writeto(Audio_U1, '0')
buf_3[0] = 192
buf_3[1] = 63
buf_3[2] = 255
i2c.writeto(Audio_U1, buf_3)
buf_3[0] = 192
buf_3[1] = 0
buf_3[2] = 0
i2c.writeto(Audio_U1, buf_3)

Loop_count = 0
while (Loop_count < 1):
    
    i2c.writeto_mem(J45_Odd, 2, b'\x00\x00')
    #i2c.writeto_mem(J45_Odd, 3, '0')
    
    i2c.writeto_mem(J48_Even, 3, b'\x00\x00')
    
    i2c.writeto_mem(J46_Even, 2, b'\x00\x00')
    #i2c.writeto_mem(J46_Even, 3, '0')
    
    i2c.writeto_mem(J46_Odd, 2, b'\x00\x00')
    #i2c.writeto_mem(J46_Odd, 3, '0')
    
    i2c.writeto_mem(J47_Even, 2, b'\x00\x00')
    #i2c.writeto_mem(J47_Even, 3, '0')
    
    i2c.writeto_mem(J47_Odd, 2, b'\x00\x00')
    #i2c.writeto_mem(J47_Odd, 3, '0')
    
    #print (Loop_count)
    time.sleep(1)
    
    i2c.writeto_mem(J45_Odd, 2, b'\xff\xff')
    #i2c.writeto_mem(J45_Odd, 3, b'\xff')
    
    i2c.writeto_mem(J48_Even, 3, b'\xff\xff')
    
    i2c.writeto_mem(J46_Even, 2, b'\xff\xff')
    #i2c.writeto_mem(J46_Even, 3, b'\xff')
    
    i2c.writeto_mem(J46_Odd, 2, b'\xff\xff')
    #i2c.writeto_mem(J46_Odd, 3, b'\xff')
    
    i2c.writeto_mem(J47_Even, 2, b'\xff\xff')
    #i2c.writeto_mem(J47_Even, 3, b'\xff')
    
    i2c.writeto_mem(J47_Odd, 2, b'\xff\xff')
    #i2c.writeto_mem(J47_Odd, 3, b'\xff')
    
    time.sleep(1)

    Loop_count += 1
 
i2c.writeto_mem(J45_Odd, 2, b'\xff\x00')
#i2c.writeto_mem(J45_Odd, 3, b'\xff')
    
i2c.writeto_mem(J48_Even, 3, b'\xf0\xf0')
    
i2c.writeto_mem(J46_Even, 2, b'\x01\xf0')
#i2c.writeto_mem(J46_Even, 3, '1')
  
i2c.writeto_mem(J46_Odd, 2, b'\xff\xe0')
#i2c.writeto_mem(J46_Odd, 3, b'\xff')
    
i2c.writeto_mem(J47_Even, 2, b'\x00\x00')
#i2c.writeto_mem(J47_Even, 3, '0')
     
#i2c.writeto_mem(J47_Odd, 2, b'\xc0\xc0')i2c.writeto_mem(J47_Odd, 3, b'\xc0')
 
buf_3[0] = 192
buf_3[1] = 42
buf_3[2] = 170
i2c.writeto(Audio_U1, buf_3)
byte_count = 0
while True:
    
    #  Read Inputs
    
    i2c_Data_In = i2c.readfrom_mem(J48_Odd, 0, 2, addrsize=8)
    K3_Band_MR_ML = i2c_Data_In[0]
    K3_Band_R_L = i2c_Data_In[1]
    
    i2c_Data_In = i2c.readfrom_mem(J45_Even, 0, 2, addrsize=8)
    PTT_WK_L = (i2c_Data_In[0] & 32) >> 5
    PTT_WK_R = (i2c_Data_In[0] & 64) >> 6
    Foot_Switch = 0
    if ((i2c_Data_In[0] & 128) >> 7) == 0:
        Foot_Switch = 1
    
    i2c_Data_In = i2c.readfrom_mem(J48_Even, 0, 2, addrsize=8)
    PTT_MR = 0
    if ((i2c_Data_In[0] & 128) >> 7) == 0:
        PTT_MR = 1
    PTT_R  = 0
    if ((i2c_Data_In[0] & 64) >> 6) == 0:
       PTT_R  = 1 
    PTT_L = 0
    if ((i2c_Data_In[0] & 32) >> 5) == 0:
        PTT_L = 0   ##### note this fix
    PTT_ML = 0
    if ((i2c_Data_In[0] & 16) >> 4) == 0:
        PTT_ML = 1
    Watt_PTT_In =i2c_Data_In[0]

    Old_Band_MR_ML = K3_Band_MR_ML
    Old_Band_R_L = K3_Band_R_L
    
    i2c_Data_In = i2c.readfrom_mem(J48_Odd, 0, 2, addrsize=8)
    K3_Band_MR_ML = i2c_Data_In[0]
    K3_Band_R_L = i2c_Data_In[1]
    
	# Read Serial Port
	
    if Use_Wifi != 1:
        Serial_Data_Rec = 0
        while uart.any() > 0:
            buf = uart.read(1)
	
        uart.write('C')
	
    #poll = select.poll()
    #poll.register(uart, select.POLLIN)
    #poll.poll(5000)
        
        try:
            uart.readinto(Read_Data,1)
            #print(Read_Data)
        except:
            print('Read timed out')
        else:
            if Read_Data[0] == 65:
 #               Loop_Count = 0
 #               Check_Sum = 0
                #print('Got this far')
                uart.readinto(Read_Data,6)
            else:
                print('Serial header is not A')
                #print(Read_Data)
 #               while uart.any() >= 6:
            
 #                   while Loop_Count < 6:
 #                       buf = uart.read(1)
 #                       Read_Data[Loop_Count] = buf[0]
 #                       if Loop_Count != 5:
 #                           Check_Sum += Read_Data[Loop_Count]
                        #print(Read_Data[Loop_Count])
 #                       Loop_Count += 1
                        #print(buf[0])
                        #buf = uart.read(1)
                        #Read_Data[Loop_Count] = buf[0] 
            
 #               if uart.any() > 0: 		# Catch up if fell behind
 #                   print('Not good')
 #                   print(uart.any())
 #                   buf = uart.read(1)
 #                   Check_Sum = 0
 #                   Loop_Count = 0
                
 #               Serial_Data_Rec = 1
                
    else:	# Using Wifi
        try:
            MCB.write('C')
            
        except:
            print('write failed')
            MCB.close()
            MCB.connect(Sockaddr)
        else:
            try:
                #print('Got Here')
                MCB.readinto(buf)
            except:
                print('Read failed')
                MCB.close()
                MCB.connect(Sockaddr)    
            else:
                if buf[0] == 65:
                    MCB.readinto(Read_Data,6)
                else:
                    print('TCP header is not A')
                
    Check_Sum = 0
    Loop_Count = 0
    while Loop_Count < 5:
        Check_Sum += Read_Data[Loop_Count]
        Loop_Count += 1
                
    Check_Sum = Check_Sum & 255
    #print(Check_Sum)        
    if Read_Data[5] == Check_Sum:
        Serial_Data_Rec = 1
        #print('Got this far - checksum')
        #byte_count += 1
        #print(byte_count)
        VB_Band = (Read_Data[0] * 256) + Read_Data[1]
           
        L_R = Read_Data[2] & 1
        Bev_R = (Read_Data[2] & 4) >> 2
        Bev_L = (Read_Data[2] & 8) >> 3
        RX_Ant_Dir_Lo = (Read_Data[2] & 16) >> 4
        RX_Ant_Dir_Hi = (Read_Data[2] & 32) >> 5
        Auto_PTT = (Read_Data[2] & 64) >> 6
        HP_Split = (Read_Data[2] & 128) >> 7
           
        Amp_Sel_L = Read_Data[3] & 1
        Amp_Sel_R = (Read_Data[3] & 2) >> 1
        Multi = ((Read_Data[3] & 4) >> 2) ^ 1
        Remote = (Read_Data[3] & 8) >> 3
           # Use audio amp on bit to control CPU vs K3 mic
        Audio_Amp_on = int((Read_Data[3] & 16) / 16)
        RX_Local_Pre_on = int((Read_Data[3] & 32) / 32)
        TX_INH_EN = int((Read_Data[3] & 64) / 64)
        K3_PWR_ON = int((Read_Data[3] & 128) / 128)
           
        Mode_bits_1 = Read_Data[4]
        Bev_MR = Read_Data[4] & 1
        Bev_ML= (Read_Data[4] & 2) >> 1
        CPU_Mic = (Read_Data[4] & 64) >> 6
           
    else:
        print('CheckSum mismatch') 
        print(Read_Data)
        print (Check_Sum)
    # Calculate the Bands
            
        #sys.exit("Error message")
    # ' No MR Band Input
         
    if ((K3_Band_MR_ML >> 4) == 0) or ((K3_Band_MR_ML >> 4) == 15):	
        K3_Band_MR_ML = K3_Band_MR_ML & 15
        K3_Band_MR_ML = K3_Band_MR_ML + (((VB_Band) & 15) << 4)
        
            # ' No ML Band Input
            
    if ((K3_Band_MR_ML & 15) == 0) or ((K3_Band_MR_ML & 15) == 15):
        K3_Band_MR_ML = K3_Band_MR_ML & 240
        K3_Band_MR_ML = K3_Band_MR_ML + (((VB_Band) & 240) >> 4)
        
    
            # ' No R Band Input
            
    if ((K3_Band_R_L >> 4) == 0) or ((K3_Band_R_L >> 4) == 15):
        K3_Band_R_L = K3_Band_R_L & 15
        K3_Band_R_L = K3_Band_R_L + (((VB_Band >> 8) & 15) << 4)
        
            # ' No L Band Input
            
    if ((K3_Band_R_L & 15) == 0) or ((K3_Band_R_L & 15) == 15):
        K3_Band_R_L = K3_Band_R_L & 240
        K3_Band_R_L = K3_Band_R_L + (((VB_Band >> 8) & 240) >> 4)
       
    ML_Bnd_Conflict = 0
    MR_Bnd_Conflict = 0
    L_Bnd_Conflict = 0
    R_Bnd_Conflict = 0
    
    if Multi == 0:
        
        # SIngle Op L and R Radios
        
        L_Band = K3_Band_R_L & 15
        R_Band = K3_Band_R_L >> 4
        if L_Band == R_Band:
            if L_R == 1:
                L_Bnd_Conflict = 1
                R_Bnd_Conflict = 1
                if L_Band == Band_160:
                    R_Band = Band_80
                else:
                    R_Band = Band_160
            else:
                L_Bnd_Conflict = 1
                R_Bnd_Conflict = 1
                if R_Band == Band_160:
                    L_Band = Band_80
                else:
                    L_Band = Band_160
                    
            K3_Band_R_L = R_Band * 16
            K3_Band_R_L = K3_Band_R_L + L_Band      
         
         # Control third RX radio
         
        ML_Band = K3_Band_MR_ML & 15
        if ML_Band == L_Band:
                ML_Bnd_Conflict = 1
                if ML_Band == Band_160:
                    if R_Band == Band_80:
                        ML_Band = Band_40
                    else:
                        ML_Band = Band_80
                elif R_Band == Band_160:
                    if L_Band == Band_80:
                        ML_Band = Band_40
                    else:
                        ML_Band = Band_80
                else: 
                    ML_Band = Band_160
        if ML_Band == R_Band:
            ML_Bnd_Conflict = 1
            if ML_Band == Band_160:
                if L_Band == Band_80:
                    ML_Band = Band_40
                else:
                    ML_Band = Band_80
            elif L_Band == Band_160:
                if R_Band == Band_80:
                    ML_Band = Band_40
                else:
                    ML_Band = Band_80
            else: 
                ML_Band = Band_160     
        K3_Band_MR_ML = (K3_Band_MR_ML & 240) + ML_Band
    else:
        # Old Multi mode (Cables moved)
        #	Band that changes last gets lower priority
        if (Mode_bits_1 & 4) != 0:
            L_Band = K3_Band_R_L & 15
            R_Band = K3_Band_R_L >> 4
            if Band_L == Band_R:
                R_Old = Old_Band_R_L >> 4
                if R_Band != R_Old:			# Right Side Changed
                    R_Bnd_Conflich = 1
                    if L_Band == Band_160:
                        R_Band = Band_80
                    else:
                        R_Band = Band_160
                else:						# (Left Both Neither) Side changed
                    L_Bnd_Conflich = 1
                    if R_Band == Band_160:
                        L_Band = Band_80
                    else:
                        L_Band = Band_160
                K3_Band_R_L = R_Band * 16
                K3_Band_R_L = K3_Band_R_L + L_Band
			# Third Radio
			# 	Put on 40 if 80 and 160 used by other radios
			#	Other radios have been adjusted so they can't be on same band
            MR_Band = K3_Band_MR_ML >> 4
            if MR_Band == L_Band:
                MR_Bnd_Conflict = 1
                if ML_Band == Band_160:		# Are they on 160
                    if R_Band == Band_80:	# Is 80 also being used
                        MR_Band = Band_40
                    else:
                        MR_Band = Band_80
                elif R_Band == Band_160:
                    if L_Band == Band_80:
                        MR_Band = Band_40
                    else:
                        MR_Band = Band_80
                else:
                    MR_Band = Band_160

            MR_Band = K3_Band_MR_ML >> 4
            if MR_Band == R_Band:
                MR_Bnd_Conflict = 1
                if ML_Band == Band_160:		# Are they on 160
                    if L_Band == Band_80:	# Is 80 also being used
                        MR_Band = Band_40
                    else:
                        MR_Band = Band_80
                elif L_Band == Band_160:
                    if L_Band == Band_80:
                        MR_Band = Band_40
                    else:
                        MR_Band = Band_80
                else:
                    MR_Band = Band_160          
                        
            K3_Band_MR_ML = K3_Band_MR_ML & 15
            K3_Band_MR_ML = K3_Band_MR_ML + (Temp_2 << 4)
        else:
            # Pure Mode Multi
            ML_Band = K3_Band_MR_ML & 15
            L_Band = K3_Band_R_L & 15
            if ML_Band == L_Band:
                if L_Band == (Old_Band_R_L & 15):		# Left side changed
                    L_Bnd_Conflict = 1
                    if ML_Band == Band_160:
                        L_Band = Band_80
                    else:
                        L_Band = Band_160
                else:
                    ML_Bnd_Conflict = 1					# ML or Both changed
                    if L_Band == Band_160:
                        ML_Band = Band_80
                    else:
                        ML_Band = Band_160
                K3_Band_R_L = (K3_Band_R_L & 240) + L_Band
                K3_Band_MR_ML = (K3_Band_MR_ML & 240) + ML_Band
            
            # Control Third Radio
            
            R_Band = K3_Band_R_L >> 4
            if R_Band == ML_Band:						# R and ML on same Band
                R_Bnd_Conflict
                if R_Band == Band_160:					# Are they on 160
                    if L_Band == Band_80:
                        R_Band = Band_40
                    else:
                        R_Band = Band_80
                elif L_Band == Band_160:
                    if ML_Band == Band_80:
                       R_Band = Band_40
                    else:
                       R_Band = Band_80
                else:
                    R_Band = Band_160
            if R_Band == L_Band:
                R_Bnd_Conflict = 1
                if R_Band == Band_160:
                    if ML_Band == Band_80:
                        R_Band = Band_40
                    else:
                        R_Band = Band_80
                elif ML_Band == Band_160:
                    if L_Band == Band_80:
                        R_Band = Band_40
                    else:
                        R_Band = Band_80
                else:
                    R_Band = Band_160
            K3_Band_R_L = K3_Band_R_L & 15
            K3_Band_R_L = K3_Band_R_L + (R_Band >> 4)
        
        # Calculate BPF Codes for adjusted bands
        
    J47_U24 = J47_U24 & 65280  # FF00
    if (K3_Band_MR_ML & 15) == Band_10:		#ML
            J47_U24 = J47_U24 + BPF_10            
    elif (K3_Band_MR_ML & 15) == Band_15:
            J47_U24 = J47_U24 + BPF_15
    elif (K3_Band_MR_ML & 15) ==  Band_20:
            J47_U24 = J47_U24 + BPF_20  
    elif (K3_Band_MR_ML & 15) ==  Band_40:
            J47_U24 = J47_U24 + BPF_40
    elif (K3_Band_MR_ML & 15) ==  Band_80:
            J47_U24 = J47_U24 + BPF_80  
    elif (K3_Band_MR_ML & 15) ==  Band_160:
            J47_U24 = J47_U24 + BPF_160              
    if RX_Ant_Dir_Hi == 0:
            J47_U24 = J47_U24 + 64
    if RX_Ant_Dir_Lo == 0:
            J47_U24 = J47_U24 + 128
                
    J47_U20 = J47_U20 & 255  # 00FF
    if (K3_Band_MR_ML >> 4) == Band_10:			# MR
            J47_U20 = J47_U20 + (BPF_10 * 256)          
    elif (K3_Band_MR_ML >> 4) == Band_15:
            J47_U20 = J47_U20 + (BPF_15 * 256)
    elif (K3_Band_MR_ML >> 4) ==  Band_20:
            J47_U20 = J47_U20 + (BPF_20 * 256) 
    elif (K3_Band_MR_ML >> 4) ==  Band_40:
            J47_U20 = J47_U20 + (BPF_40 * 256)
    elif (K3_Band_MR_ML >> 4) ==  Band_80:
            J47_U20 = J47_U20 + (BPF_80 * 256)  
    elif (K3_Band_MR_ML >> 4) ==  Band_160:
            J47_U20 = J47_U20 + (BPF_160 * 256)
              
    J47_U20 = J47_U20 + (RX_Local_Pre_on *64 * 256)
    if Mode_bits_1 == 4:
        J47_U20 = J47_U20 + 32768 	# 8000
    else:
        J47_U20 = J47_U20 & 32767	# 7FFF
            
    J47_U24 = J47_U24 & 255  # 00FF
    if (K3_Band_R_L & 15) == Band_10:			# L
            J47_U24 = J47_U24 + (BPF_10 * 256)          
    elif (K3_Band_R_L & 15) == Band_15:
            J47_U24 = J47_U24 + (BPF_15 * 256)
    elif (K3_Band_R_L & 15) == Band_20:
            J47_U24 = J47_U24 + (BPF_20 * 256) 
    elif (K3_Band_R_L & 15) == Band_40:
            J47_U24 = J47_U24 + (BPF_40 * 256)
    elif (K3_Band_R_L & 15) == Band_80:
            J47_U24 = J47_U24 + (BPF_80 * 256)  
    elif (K3_Band_R_L & 15) == Band_160:
            J47_U24 = J47_U24 + (BPF_160 * 256)
        
    if Remote == 0:
        J47_U24 = J47_U24 + (64 * 256)
    J47_U24 = J47_U24 + (Audio_Amp_on * 128 * 256)
        
        
    J47_U20 = J47_U20 & 65280  # FF00
    if (K3_Band_R_L >> 4) == Band_10:			# R
            J47_U20 = J47_U20 + BPF_10            
    elif (K3_Band_R_L >> 4) == Band_15:
            J47_U20 = J47_U20 + BPF_15
    elif (K3_Band_R_L >> 4) == Band_20:
            J47_U20 = J47_U20 + BPF_20  
    elif (K3_Band_R_L >> 4) == Band_40:
            J47_U20 = J47_U20 + BPF_40
    elif (K3_Band_R_L >> 4) == Band_80:
            J47_U20 = J47_U20 + BPF_80  
    elif (K3_Band_R_L >> 4) == Band_160:
                J47_U20 = J47_U20 + BPF_160 
         
         
    J47_U24 = J47_U24 & (65535 - 24)   # FFE7
    if ((Mode_bits_1 & 24) >> 3) == 0:		# Use Spare 6 for Amp(RL)_ON
                J45_U26 = J45_U26 + 3
    elif ((Mode_bits_1 & 24) >> 3) == 1:
                J45_U26 = J45_U26 + 2
    elif ((Mode_bits_1 & 24) >> 3) == 2:
                 J45_U26 = J45_U26 + 1
    elif ((Mode_bits_1 & 24) >> 3) == 3:
                 J45_U26 = J45_U26 + 0
                 
 #       if (Mode_Bits & 128) != 128:  # Radio Left/Right
    if L_R == 0:
        L_R = 0
        J46_U21 = 32
    else:
        L_R = 1
        J46_U21 = 16
             
    J45_U26 = J45_U26 | 4			# Use Spare 7 Tip/Ring For ACOM
    if (Mode_bits_1 & 32) == 32:				# Pulse ACOM L
        J45_U26 = J45_U26 & (65535 - 4) # FFFB
                
    J45_U26 = J45_U26 | 8			# Use Spare 7 Tip/Ring For ACOM
    if (Mode_bits_1 & 128) == 128:				# Pulse ACOM R
        J45_U26 = J45_U26 & (65535 - 8) # FFF7
            
    J45_U26 = J45_U26 & (65535 - 48) # FFCF
    if Amp_Sel_L == 0:
        J46_U21 = J46_U21 + 64
        J45_U26 = J45_U26 | 16
            
    if Amp_Sel_R == 0:
        J46_U21 = J46_U21 + 128
        J45_U26 = J45_U26 | 32
            
    J45_U26 = J45_U26 & (63)  # 3F
    if RX_Ant_Dir_Lo == 0:		# Dont know what this is
        J45_U26 = J45_U26 + 128 # Spare 9
    else:
        J45_U26 = J45_U26 + 64
            
    J45_U26 = J45_U26 * 256
    J46_U23 = J46_U23 & 255
        
    J46_U23 = J46_U23 + ((Remote | CPU_Mic) * 64 * 256)
            
    if Multi == 0:
        J46_U23 = J46_U23 | 512
    else:
        J46_U23 = J46_U23 & (65535 - 512)
        
        J48_U29_P1 = 240 + (K3_PWR_ON & 15)  # F0
                                 
    J48_U29_P1 = J48_U29_P1 & 63 	# 3F
    if RX_Ant_Dir_Lo == 0:
        J48_U29_P1 = J48_U29_P1 | 128
    if RX_Ant_Dir_Hi == 0:
        J48_U29_P1 = J48_U29_P1 | 64
                                 
      # Amp Relays
#;************************************************************************************
#;
#;	Control Amplifier radios and K3 TX Inhibit
#;
#;		Disable amplifier relays is Band Conflict or Wattmeter Fault
#;
#;		If TX inhibit is enabled, set TX Inhibit on Conflict and Wattmeter Fault
#;	Beverage Select
#;		
#;		Select Beverages only if on 80 and 160 (Now Select on all bands)
#;************************************************************************************
                                 
        #' Amp Relays 	MR, R, L, ML, XXXX
        #' TX INH		XX, ML, MR, L, R, XX
                                 
    J46_U23 = J46_U23 & 49935 	# C30F
    Temp_1 = 0                         
    if (ML_Bnd_Conflict == 1) or ((Watt_PTT_In & 1) == 1):
            J46_U23 = J46_U23 + 16
            Temp_1  = Temp_1 + 32
                                 
    if (MR_Bnd_Conflict == 1) or ((Watt_PTT_In & 8) == 8):
            J46_U23 = J46_U23 + 128
            Temp_1  = Temp_1 + 16
                                 
    if (L_Bnd_Conflict == 1) or ((Watt_PTT_In & 2) == 2):
            J46_U23 = J46_U23 + 32
            Temp_1  = Temp_1 + 8
                                 
    if (R_Bnd_Conflict == 1) or ((Watt_PTT_In & 4) == 4):
            J46_U23 = J46_U23 + 64
            Temp_1  = Temp_1 + 4
        
    J47_U20 = J47_U20 & (65535 - 64 - 128)
    if TX_INH_EN == 1:
            J46_U23 = J46_U23 + (Temp_1 * 256)
            J47_U20 = J47_U20 + ((Temp_1 & 8) * 8)		# TX INH H L
            J47_U20 = J47_U20 + ((Temp_1 & 4) * 32)		# TX INH H R
        
    J46_U23 = J46_U23 & (65535 - 4)
    if ((K3_Band_R_L & 15) <= Band_40) and (L_Bnd_Conflict == 0):
            J46_U23 = J46_U23 + (Bev_L * 4)
                                     
    J46_U23 = J46_U23 & (65535 - 8)
    if ((K3_Band_R_L >> 4) <= Band_40) and (R_Bnd_Conflict == 0):
            J46_U23 = J46_U23 + (Bev_R * 8)
                                     
    J46_U23 = J46_U23 & (65535 - 1)
    if ((K3_Band_MR_ML & 15) <= Band_40) and (ML_Bnd_Conflict == 0):
            J46_U23 = J46_U23 + (Bev_ML * 1)
                                     
    J46_U23 = J46_U23 & (65535 - 2)
    if ((K3_Band_MR_ML >> 4) <= Band_40) and (MR_Bnd_Conflict == 0):
            J46_U23 = J46_U23 + (Bev_MR * 2)  

#;*****************************************************************************************************
#;
#;	Control Headphones
#;
#;	If HP_Split asserted, Split headphones and disable Automation
#;
#;	If Automated
#;		If No PTT 
#;			if no Foot Switch, headphones on Active radio
#;			If Footswitch on, Headphones on inactive radio
#;	
#;		If PTT On
#;			if no footswitch on (or was on) nor Auto PTT, Headphones on Active radio
#;			Footswitch on or previously pressed, or Auto PTT, Headphones on inactive radio
#;		
#;*****************************************************************************************************
                                     
   # HP Control
   
    if HP_Split == 1:
        if Auto_PTT == 1:
            if PTT_WK_L == 1:
                HP_L_Sel = 0
                HP_R_Sel = 0
            elif PTT_WK_R == 1:
                HP_L_Sel = 1
                HP_R_Sel = 1
            else:
                if (PTT_WK_R == 0) and (PTT_WK_L == 0):
                    HP_L_Sel = 1
                    HP_R_Sel = 0
        else:
            HP_L_Sel = 1
            HP_R_Sel = 0
    else:				# Automatic mode
        if (PTT_WK_R == 0) and (PTT_WK_L == 0):
            Foot_Lock = 0
            if Foot_Switch == 0:	#No Swap
                HP_L_Sel = L_R
                HP_R_Sel = L_R
            else:
                HP_L_Sel = (L_R + 1) & 1 # Invert
                HP_R_Sel = (L_R + 1) & 1
        else:
            if Foot_Switch == 1:
                Foot_Lock = 1
            if (Auto_PTT == 0) and (Foot_Lock == 0):
                HP_L_Sel = L_R
                HP_R_Sel = L_R
            else:
                HP_L_Sel = (L_R + 1) & 1 # Invert
                HP_R_Sel = (L_R + 1) & 1               
        
     # Audio I2C
     
    buf_3[0] = 192
    if Multi == 0:
        if L_R == 1:
            buf_3[1] = 15	# 5 on = Left Mic
        else:
            buf_3[1] = 32	# 8 on = Left Mic
    else:
        if (Mode_bits_1 & 4) != 0:	# Multi Old
            buf_3[1] = 32			# Right Mic
        else:						# Pure Multi
            buf_3[1] = 16			# Left Mic
    if Audio_Amp_on == 1:
        buf_3[1] = buf_3[1] + 5		# 7A and 6A
        buf_3[2] = 80				# 4A and 3A
    else:
        buf_3[1] = buf_3[1] + 10		# 7B and 6B
        buf_3[2] = 80				# 4B and 3B
        
    if Multi == 0:
        if HP_L_Sel == HP_R_Sel:
            if HP_L_Sel == 0:
                buf_3[2] = buf_3[2] + 10	# 2B and 1B Both Right
            else:
                buf_3[2] = buf_3[2] + 5		# 2A and 1A Both Left
        else:
                buf_3[2] = buf_3[2] + 9		# 2B and 1A Split
    else:
        if (Mode_bits_1 & 4) != 0:
                buf_3[2] = buf_3[2] + 10	# 2B and 1B Both Right
        else:
                buf_3[2] = buf_3[2] + 5		# 2A and 1A Both Left
        
    i2c.writeto(Audio_U1, buf_3)
 
#'***********************************************************************************
#'
#'	Switch in BPF for the Beverage signal
#'
#'	In the single Op on Old Multi cases
#'	
#'		If either Radio is using a Beverage , Filter may be necessary
#'	
#'		If neither PTT Selected
#'			Bypass filters
#'
#'		If Either PTT indicates transmitting on 80 or 160, 
#'			If other radio is using a Beverage, then switch in appropriate filter.
#'
#'***********************************************************************************
    Temp_0 = 0
    J47_U20 = J47_U20 & 49407 		# C0FF -  MR
    if (((((Mode_bits_1 & 4) >> 4) + 1) & 1) & Multi) == 0:	#  SO2R or Old Multi
        if (Bev_L | Bev_R) == 1:
            if (PTT_R & Bev_L) == 1:
                if (J47_U20 & 63) > 8:			# R Radio on 80 or 160
                    if ((J47_U24 >> 8) & 63) == BPF_80:
                        Temp_0 = BPF_80 * 256
                    if ((J47_U24 >> 8) & 63) == BPF_160:
                        Temp_0 = BPF_80 * 256
                    Temp_0 = ((J47_U24 >> 8) & 63) * 256
            if (PTT_L & Bev_R) == 1:
                if ((J47_U24 >> 8) & 63) > 8:			# L Radio on 80 or 160
                    if (J47_U20 & 63) == BPF_80:
                        Temp_0 = BPF_80 * 256
                    if (J47_U20 & 63) == BPF_160:
                        Temp_0 = BPF_80 * 256
                    Temp_0 = ((J47_U20 >> 8) & 63) * 256
    else:	# Multi New - USE ML and L
        if (Bev_L | Bev_ML) == 1:
            if (PTT_ML & Bev_L) == 1:
                if (J47_U24 & 63) > 8:			# ML Radio on 80 or 160
                    if ((J47_U24 >> 8) & 63) == BPF_80:
                        Temp_0 = BPF_80 * 256
                    if ((J47_U24 >> 8) & 63) == BPF_160:
                        Temp_0 = BPF_80 * 256
                    Temp_0 = ((J47_U24 >> 8) & 63) * 256
            if (PTT_L & Bev_ML) == 1:
                if ((J47_U24 >> 8) & 63) > 8:			# L Radio on 80 or 160
                    if (J47_U24 & 63) == BPF_80:
                        Temp_0 = BPF_80 * 256
                    if (J47_U24 & 63) == BPF_160:
                        Temp_0 = BPF_80 * 256
                    Temp_0 = ((J47_U24 >> 8) & 63) * 256
    J47_U20 = J47_U20 + Temp_0
    
    # Serial / I2C outputs
       
    Check_Sum = 0
                        
    if Serial_Data_Rec == 1:
        if Use_Wifi == 1:
            MCB.write('D')
        else:
            uart.write('D')
        
        buf_8[0] = Bev_MR + (Bev_ML * 2)+ (Bev_R * 4)+ (Bev_L * 8) + (R_Bnd_Conflict * 16) + (L_Bnd_Conflict * 32) + (MR_Bnd_Conflict * 64) + (ML_Bnd_Conflict * 128)                                           
        buf_8[1] = K3_Band_MR_ML
        buf_8[2] = K3_Band_R_L
        buf_8[3] = TX_INH_EN + (Auto_PTT * 2)+ (HP_R_Sel * 4)+ (HP_L_Sel * 8) + (PTT_R * 16)\
                    + (PTT_L * 32) + (PTT_MR * 64) + (PTT_ML * 128)                                      
        buf_8[4] = Foot_Lock + (HP_Split * 2)+ (Amp_Sel_L * 4)+ (Amp_Sel_R * 8) + (Serial_Data_Rec * 16)\
                    + (Foot_Switch * 32) + (PTT_WK_R * 64) + (PTT_WK_L * 128)
        
        Loop_Count = 0
        while (Loop_Count < 5):
            Check_Sum += buf_8[Loop_Count]
            Loop_Count += 1
            
        i2C_Data_Out[1] = J45_U26 >> 8
        i2C_Data_Out[0] = J45_U26 & 255
        i2c.writeto_mem(J45_Odd, 2, i2C_Data_Out)
                                               
        buf_8[5] = J46_U23 & 255
        i2C_Data_Out[1] = J46_U23 >> 8
        i2C_Data_Out[0] = J46_U23 & 255
        #uart.write(i2C_Data_Out[1])
        Check_Sum += buf_8[5]
        i2c.writeto_mem(J46_Even, 2, i2C_Data_Out)
        
        buf_8[6] = J46_U21 & (255 - 16)
        if (J46_U21 & 16) == 0:   # Flip *L_out which is R_Sel
            buf_8[6] = buf_8[6] + 16
        i2C_Data_Out[1] = J46_U21 >> 8
        i2C_Data_Out[0] = buf_8[6]
        #uart.write(i2C_Data_Out[1])
        Check_Sum += buf_8[6]
        i2c.writeto_mem(J46_Odd, 2, i2C_Data_Out)
        
        buf_8[7] = J47_U24 & 255
        i2C_Data_Out[1] = J47_U24 >> 8
        i2C_Data_Out[0] = buf_8[7]
        #uart.write(i2C_Data_Out[1])
        Check_Sum += buf_8[7]
        i2c.writeto_mem(J47_Odd, 2, i2C_Data_Out)
        
        i2C_Data_Out[1] = J47_U20 >> 8
        i2C_Data_Out[0] = J47_U20 & 255
        i2c.writeto_mem(J47_Even, 2, i2C_Data_Out)
        
        i2C_Data_Out[1] = J48_U29_P1 >> 8
        i2C_Data_Out[0] = J48_U29_P1 & 255
        i2c.writeto_mem(J48_Even, 2, i2C_Data_Out)
        
        Check_Sum = Check_Sum & 255
        buf_8[8] = Check_Sum
        if Use_Wifi == 1:
            MCB.write(buf_8)
        else:
            uart.write(buf_8)
        Serial_Data_Rec = 0
        J46_U23 = 0
        #print('J47_U20 = ', hex(J47_U20))
        #print('J47_U24 = ', hex(J47_U24))
        #print('J45_U26 = ', hex(J45_U26))
        #print('J46_U21 = ', hex(J46_U21))
        #print('J48_U29_P1 = ', hex(J48_U29_P1))
        