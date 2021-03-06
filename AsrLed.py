#!/usr/bin/python#!/usr/bin/python

# AsrLed nu51_1.10 Driver for Linux
# 2019 (c) Erdem Umut Altunyurt
#
#    This is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You can share it under GNU General Public License v3
#    If not know what it is, see <https://www.gnu.org/licenses/>.
#

# Notices: This driver just for AsRock Fatal1ty AB350 Gaming-ITX/ac board.
# But probably compatible with all AsRock Motherboards that runs AsrRgbLed utility.
#
# If you change RGB values too much, for example using set_static_rgb register in a programatic loop to animate your custom choice,
# you *PROBABLY* kill your RGB Controller MCU EEPROM, that might lead some errors on RGB LED Lightning...
#
# Warning: Motherboards that run AsrPolychromeRGB runs nu51_2.10 or nu51_3.00 firmware does NOT tested with this driver. Probably not fully compatible.
#
# Register 0x30 controls the device mode. Following RGB code (if exist) and Speed code (if exist). Speed is higher with lower values.
# I don't understand what the Reg 0x31 for, and 0x32 used by original firmware but things look working pretty good without it.

from smbus import SMBus
from time import sleep
import random,psutil,os,time

os.system("/bin/modprobe i2c-dev")

addr=0x6a
bus=-1
def detect_device():
  for busNum in range(20):
    if not os.path.exists('/dev/i2c-' + str(busNum)):
      if busNum==20-1:
        print("device not found.")
        return -1
      continue
    bus = SMBus(busNum)
    print("Bus #{} open. Searching...".format(busNum))
    response = bus.read_byte(addr)
    if response >= 0:
      #print("On bus {} a device {} found with response of {}".format(busNum, hex(dev_addr), hex(response)))
      if bus.read_byte_data( addr,0x00)==2:
         M=bus.read_byte( addr )
         m=bus.read_byte( addr )
         print("Bus:{} Addr:{} Reg:0x00 query returns {}.{}.\nPossible AsRock AURA device with FW nu50_{}.{} detected.".format(busNum, hex(addr), M, m, M, m))
         if M!=1 and m!=10:
           print("This FW is NOT supported, yet. Try with your own risk!")
         return bus
    bus.close()

bus = detect_device()
#bus=SMBus(2)

def fw_ver():
  bus.read_byte_data( addr, 0x0 )
  M=bus.read_byte( addr ) 
  m=bus.read_byte( addr )
  print( "Firmware: {}.{}".format(M,m) )

mode = {'off':0x10,
	'static':0x11,
	'breathing':0x12,
	'strobe':0x13,
	'cycling':0x14,
	'random':0x15,
	'music':0x17,
	'wave':0x18}

def dump():
  for i in range(0,0xff):
    a=bus.read_byte_data( addr, i )
    if(a!=0):
      print( hex(i),':',end='')
      for i in range(a):
        ret=bus.read_byte(addr)
        print(hex(ret),end=' ')
      print('')

def get_mode():
  bus.read_byte_data( addr, 0x30 )
  ret=bus.read_byte(addr)
  ret=list(mode.keys())[list(mode.values()).index(ret)]
  return ret

def set_mode( new_mode ):
  bus.write_block_data( addr, 0x30, [mode.get(new_mode)] )

def set_off():
  set_mode('off')

def set_static_rgb(r,g,b):
  set_mode('static')
  bus.write_block_data( addr, 0x11, [r,g,b] )

def set_breathing_rgbs(r,g,b,s):
  set_mode('breathing')
  bus.write_block_data( addr, 0x12, [r,g,b,s] )

def set_strobe_rgbs(r,g,b,s):
  set_mode('strobe')
  bus.write_block_data( addr, 0x13, [r,g,b,s] )

def set_cycling_rgbs(r,g,b,s):
  set_mode('cycling')
  bus.write_block_data( addr, 0x14, [r,g,b,s] )

def set_random_s(s):
  set_mode('random')
  bus.write_block_data( addr, 0x15, [s] )

def set_music_rgb(r,g,b):
  set_mode('music')
  bus.write_block_data( addr, 0x17, [r,g,b]  )

def set_wave_s(s):
  set_mode('wave')
  bus.write_block_data( addr, 0x18, [s] )

if __name__ == "__main__":
  print ("Switching Cycling Mode")
  set_mode('cycling')
  set_cycling_rgbs(10,5,5,150)
