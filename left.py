# Handles the left keyboard, i.e. the host, which includes connecting to the client, reading client data, reading its keys,
# handling key input logic and sending HID

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

	# Checks the duration the communication pin is turned on
	def next_signal_length() -> int:
		while comm_pin.value is False:
			pass
		signal_start_time = time_ms()
		while comm_pin.value is True:
			pass
		signal_end_time = time_ms()
		print(signal_end_time - signal_start_time)
		return signal_end_time - signal_start_time

	max_connect_signal_error = 1 # 1ms
	client_connected = False
	while not client_connected:
		if abs(next_signal_length() - connect_signal_duration) < max_connect_signal_error:
			client_connected = True
	origin_time = time_ms() + bit_duration # we add bit_duration to wait for the last zero-bit

def recv() -> list[bool]:
	wait_for_segment_read(origin_time)
	keys = []
	for i in range(num_buttons):
		keys.append(comm_pin.value)
		sleep_ms(bit_duration)
	return keys

# Initialize key input pins, giving them the input direction and connecting pullup resistors
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
		# Press a released left button if it had been pressed for at least press_threshhold milliseconds
		if left_keys[i] and time_ms() - left_key_starts[i] > press_threshhold and left_key_starts[i] != -1.0:
			return layer[0][i]
		# Press a released right button if it had been pressed for at least press_threshhold milliseconds
		if right_keys[i] and time_ms() - right_key_starts[i] > press_threshhold and right_key_starts[i] != -1.0:
			if i == 0: # Switch to second alpha layer after left thumb key is released
				layer = alpha2
				one_shot = True
			return layer[1][i]
	return ()

def update_key_timers():
	for i in range(num_buttons):
		# If key is released this instant, set the time when it started being held to -1
		if left_keys[i]:
			left_key_starts[i] = -1.0
		# If key is pressed this instant, set the time when it started being helt to now
		elif left_key_starts[i] == -1.0:
			left_key_starts[i] = time_ms()
		# Same as for the left keys
		if right_keys[i]:
			right_key_starts[i] = -1.0
		elif right_key_starts[i] == -1.0:
			right_key_starts[i] = time_ms()

# ( left-layout: (right-thumb, left-thumb, bottom-pinky, bottom-index, bottom-middle, bottom-ring, top-pinky, top-index, top-middle, top-ring)
# , right-layout:(left-thumb, right-thumb, bottom-pinky, bottom-index, bottom-middle, bottom-ring, top-pinky, top-index, top-middle, top-ring))
alpha1 = (
	((), Key.BACKSPACE, Key.M, Key.T, Key.S, Key.R, Key.F, Key.D, Key.L, Key.G),
	((), Key.SPACE, Key.I, Key.N, Key.E, Key.A, Key.C, Key.H, Key.U, Key.O)
)
alpha2 = (
	((), (), Key.Q, Key.K, Key.J, Key.Y, Key.X, Key.V, Key.W, Key.Z),
	((), (), Key.Å, Key.P, Key.PERIOD, Key.COMMA, Key.Ö, Key.B, Key.APOSTROPHE, Key.Ä)
)
layer = alpha1
# A one shot layer, meaning you press one key in that layer and then return to the starting layer
# The second alpha layer is a one shot layer
one_shot = False

left_key_starts = [-1.0 for _ in range(num_buttons)]
right_key_starts = [-1.0 for _ in range(num_buttons)]

wait_for_client_connection()
print("connected")

while True:
	right_keys = recv()
	left_keys = read_keys()
	keys_to_press = handle_keyboard_logic()
	if keys_to_press != ():
		# If we press a key in a one shot layer, we are returned to the first alpha layer
		if one_shot:
			one_shot = False
			layer = alpha1
		keyboard.press(*keys_to_press)
		keyboard.release(*keys_to_press)
	update_key_timers()