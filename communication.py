import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from time import sleep, time_ns

# All durations are counted in microseconds
num_buttons = 10
bits_per_segment = num_buttons
bit_duration = 500 # time between sending bits
segment_duration = bits_per_segment * bit_duration

task_duration = 10000 # time to finish other tasks than communication
time_between_segments = segment_duration + task_duration # time between sending segments

data_comm_pin = board.GP0

def sleep_us(duration):
	sleep(duration * 1e-6)

def time_us() -> int:
	return time_ns() // 1000

def wait_for_segment_send():
	current_time = time_us()
	time_since_last_segment = current_time % time_between_segments
	time_until_next_segment = time_between_segments - time_since_last_segment
	sleep_us(time_until_next_segment)

def send(bits: list[bool]): # only `num_buttons` bits will be written
	wait_for_segment_send()

	for i in range(num_buttons):
		data_comm_pin.value = bits[i]
		sleep_us(bit_duration)

def recv() -> list[bool]:
	wait_for_segment_send()
	sleep_us(bit_duration * 0.5) # ensures we don't read before written
	
	keys = []
	for _ in range(len(keys)):
		keys.append(data_comm_pin.value)
		sleep_us(bit_duration)
	return keys