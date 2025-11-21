try:
	import board
except ImportError:
	import mock_board as board

import digitalio
#import adafruit_hid.keyboard
import time

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

while True:
	led.value = True
	time.sleep(0.1)
	led.value = False
	time.sleep(0.5)