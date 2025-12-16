import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

from time import sleep, time_ns

# All durations are counted in microsecond

bits_per_segment = 10
segment_duration = 1
time_between_bits = bits_per_segment / segment_duration # time between sending bits

host_task_duration = 1000 # time the host requires to finish its tasks
time_between_segments = segment_duration + host_task_duration # time between sending segments

def sleep_us(duration):
	sleep(duration * 1e-6)

def time_us() -> int:
	return time_ns() // 1000

def wait_for_segment_send():
	current = time_us()
	time_since_last_segment = current % time_between_segments
	time_until_next_segment = time_between_segments - time_since_last_segment
	sleep_us(time_until_next_segment)

def send(pin: DigitalInOut, bits: list[bool]):
	wait_for_segment_send()

	for bit in bits:
		pin.value = int(bit)
		sleep_us(time_between_bits)

def recv(pin: DigitalInOut) -> list[bool]:
	wait_for_segment_send()
	sleep_us(time_between_bits * 0.5) # ensures we don't read before written
	
	keys = []
	for _ in range(len(keys)):
		keys.append(pin.value)
		sleep_us(time_between_bits)
	return keys