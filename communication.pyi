# Interface file for the communication functions in communication-left.py and communication-right.py

import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from time import sleep, monotonic, monotonic_ns

# All durations are counted in milliseconds
connect_signal_bit_duration: float
connect_signal_duration: float

num_buttons: int
bits_per_segment: int
bit_duration: float # time between sending bits
segment_duration: float

task_duration: float # time to finish other tasks than communication
time_between_segments: float # time between sending segments

def sleep_ms(duration) -> None:
	pass

def time_ms() -> float:
	pass

def wait_for_segment_send(origin_time: float):
	pass

def wait_for_segment_read(origin_time: float):
	pass