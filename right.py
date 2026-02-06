import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from communication import *

from time import sleep

sleep(1.0)

comm_pin = DigitalInOut(board.GP2)
comm_pin.direction = Direction.OUTPUT

origin_time = 0

def send_connect_signal():
	global origin_time
	comm_pin.value = False
	sleep_ms(bit_duration)
	start_time = time_ms()
	comm_pin.value = True
	sleep_ms(connect_signal_duration)
	end_time = time_ms()
	comm_pin.value = False
	origin_time = time_ms() + bit_duration # we wait for the zero-bit to finish
	#print(end_time - start_time)

def send(bits: list[bool]): # only `num_buttons` bits will be written
	wait_for_segment_send(origin_time)

	for i in range(num_buttons):
		#print(i, bits[i])
		comm_pin.value = bits[i]
		sleep_ms(bit_duration)

key_pin_nums = [board.GP19, board.GP14, board.GP7, board.GP27, board.GP22, board.GP21, board.GP5, board.GP28, board.GP26, board.GP4]
key_pins = [DigitalInOut(key_pin) for key_pin in key_pin_nums]

for i in range(len(key_pins)):
	key_pins[i].direction = Direction.INPUT
	key_pins[i].pull = Pull.UP

def read_keys() -> list[bool]:
	keys = [key_pin.value for key_pin in key_pins]
	return keys

send_connect_signal()
while True:
	send(read_keys())