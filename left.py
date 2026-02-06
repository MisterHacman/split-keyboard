import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

import usb_hid
from adafruit_hid.keyboard import Keyboard

from keycodes import Key
from communication import *

keyboard = Keyboard(usb_hid.devices)

comm_pin = DigitalInOut(board.GP2)
comm_pin.direction = Direction.INPUT

origin_time = 0

def wait_for_client_connection():
	global origin_time

	def next_signal_length() -> int:
		while comm_pin.value is False:
			pass
		signal_start_time = time_ms()
		while comm_pin.value is True:
			pass
		signal_end_time = time_ms()
		print(signal_end_time - signal_start_time)
		return signal_end_time - signal_start_time

	max_connect_signal_error = 1
	offset = 0
	client_connected = False
	while not client_connected:
		if abs(next_signal_length() - connect_signal_duration - offset) < max_connect_signal_error:
			client_connected = True
	origin_time = time_ms() + bit_duration # we add bit duration to wait for the last zero-bit 

def recv() -> list[bool]:
	wait_for_segment_read(origin_time)
	
	keys = []
	for i in range(num_buttons):
		keys.append(comm_pin.value)
		sleep_ms(bit_duration)
	return keys

key_pin_nums = [board.GP14, board.GP17, board.GP11, board.GP22, board.GP26, board.GP21, board.GP18, board.GP19, board.GP28, board.GP27]
key_pins = [DigitalInOut(key_pin) for key_pin in key_pin_nums]

for i in range(len(key_pins)):
	key_pins[i].direction = Direction.INPUT
	key_pins[i].pull = Pull.UP

def read_keys() -> list[bool]:
	keys = [key_pin.value for key_pin in key_pins]
	return keys

press_threshhold = 30.0

def handle_keyboard_logic() -> tuple:
	global layer, one_shot
	for i in range(num_buttons):
		if left_keys[i] and time_ms() - left_key_starts[i] > press_threshhold and left_key_starts[i] != -1.0:
			return layer[0][i]
		if right_keys[i] and time_ms() - right_key_starts[i] > press_threshhold and right_key_starts[i] != -1.0:
			if i == 0: # Switch to second alpha layer
				layer = alpha2
				one_shot = True
			return layer[1][i]
	return ()

def update_key_timers():
	for i in range(num_buttons):
		if left_keys[i]:
			left_key_starts[i] = -1.0
		elif left_key_starts[i] == -1.0:
			left_key_starts[i] = time_ms()
		if right_keys[i]:
			right_key_starts[i] = -1.0
		elif right_key_starts[i] == -1.0:
			right_key_starts[i] = time_ms()

alpha1 = (
	((), Key.BACKSPACE, Key.M, Key.T, Key.S, Key.R, Key.F, Key.D, Key.L, Key.G),
	((), Key.SPACE, Key.I, Key.N, Key.E, Key.A, Key.C, Key.H, Key.U, Key.O)
)

alpha2 = (
	((), (), Key.Q, Key.K, Key.J, Key.Y, Key.X, Key.V, Key.W, Key.Z),
	((), (), Key.Å, Key.P, Key.PERIOD, Key.COMMA, Key.Ö, Key.B, Key.APOSTROPHE, Key.Ä)
)

layer = alpha1
one_shot = False

wait_for_client_connection()

print("connected")

left_key_starts = [-1.0 for _ in range(num_buttons)]
right_key_starts = [-1.0 for _ in range(num_buttons)]

while True:
	right_keys = recv()
	left_keys = read_keys()
	keys_to_press = handle_keyboard_logic()
	if keys_to_press != ():
		if one_shot:
			one_shot = False
			layer = alpha1
		keyboard.press(*keys_to_press)
		keyboard.release(*keys_to_press)
	update_key_timers()