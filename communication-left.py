import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from time import sleep, monotonic, monotonic_ns

# All durations are counted in milliseconds
connect_signal_bit_duration = 100
connect_signal_duration = connect_signal_bit_duration * 10

num_buttons = 10
bits_per_segment = num_buttons
bit_duration = 3 # time between sending bits
segment_duration = bits_per_segment * bit_duration

task_duration = 10 # time to finish other tasks than communication
time_between_segments = segment_duration + task_duration # time between sending segments

def sleep_ms(duration):
	sleep(duration * 1e-3)

def time_ms() -> float:
	return monotonic_ns() * 1e-6

def wait_for_segment_read(origin_time: float):
	current_time = time_ms() - origin_time
	time_since_last_segment = current_time % time_between_segments
	time_until_next_segment = time_between_segments - time_since_last_segment
	#print(time_until_next_segment)
	sleep_ms(time_until_next_segment)
	sleep_ms(bit_duration * 0.5) # wait a bit after client wrote