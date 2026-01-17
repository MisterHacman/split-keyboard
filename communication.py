import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from time import sleep, monotonic_ns

# All durations are counted in microseconds
num_buttons = 10
bits_per_segment = num_buttons
bit_duration = 500 # time between sending bits
segment_duration = bits_per_segment * bit_duration

task_duration = 10000 # time to finish other tasks than communication
time_between_segments = segment_duration + task_duration # time between sending segments

def sleep_us(duration):
	sleep(duration * 1e-6)

def time_us() -> int:
	return monotonic_ns() // 1000

def wait_for_segment_send():
	current_time = time_us()
	time_since_last_segment = current_time % time_between_segments
	time_until_next_segment = time_between_segments - time_since_last_segment
	sleep_us(time_until_next_segment)