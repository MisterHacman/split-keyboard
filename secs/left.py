import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

import usb_hid
from adafruit_hid.keyboard import Keyboard

from keycodes import AnsiKey
from communication import *

from time import sleep, monotonic, monotonic_ns

keyboard = Keyboard(usb_hid.devices)

comm_pin = DigitalInOut(board.GP2)
comm_pin.direction = Direction.INPUT

origin_time = 0

def wait_for_client_connection():
	global origin_time

	def next_signal_length() -> int:
		while comm_pin.value is False:
			pass
		signal_start_time = monotonic()
		while comm_pin.value is True:
			pass
		signal_end_time = monotonic()
		print(signal_end_time - signal_start_time)
		return signal_end_time - signal_start_time

	max_connect_signal_error = 0.002
	offset = 0.004
	client_connected = False
	while not client_connected:
		if abs(next_signal_length() - connect_signal_length - offset) < max_connect_signal_error:
			client_connected = True
	origin_time = monotonic() + bit_duration # we add bit duration to wait for the last zero-bit 

def recv() -> list[bool]:
	wait_for_segment_send(origin_time)
	sleep(bit_duration * 0.5) # ensures we don't read before written
	
	keys = []
	for i in range(num_buttons):
		print(i, comm_pin.value)
		keys.append(comm_pin.value)
		sleep(bit_duration)
	return keys

def read_keys() -> list[bool]:
	pass

def handle_keyboard_logic() -> list[tuple]:
	pass

wait_for_client_connection()
while True:
	right_keys = recv()
	left_keys = read_keys()
	key_to_press = handle_keyboard_logic()
	#keyboard.press(key_to_press)
	#keyboard.release(key_to_press)