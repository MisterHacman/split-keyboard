# Contains the class for HID key aliases

import sys

if sys.implementation.name == "circuitpython":
	import board
else:
	import mock_board as board

from digitalio import DigitalInOut, Direction, Pull

def shift(self, keys):
	return self.RIGHT_SHIFT + keys
def alt(self, keys):
	return self.ALT + self.RIGHT_CTRL + keys

class Key:
	A = (0x04,)
	B = (0x05,)
	C = (0x06,)
	D = (0x07,)
	E = (0x08,)
	F = (0x09,)
	G = (0x0a,)
	H = (0x0b,)
	I = (0x0c,)
	J = (0x0d,)
	K = (0x0e,)
	L = (0x0f,)
	M = (0x10,)
	N = (0x11,)
	O = (0x12,)
	P = (0x13,)
	Q = (0x14,)
	R = (0x15,)
	S = (0x16,)
	T = (0x17,)
	U = (0x18,)
	V = (0x19,)
	W = (0x1a,)
	X = (0x1b,)
	Y = (0x1c,)
	Z = (0x1d,)

	_1 = (0x1e,)
	_2 = (0x1f,)
	_3 = (0x20,)
	_4 = (0x21,)
	_5 = (0x22,)
	_6 = (0x23,)
	_7 = (0x24,)
	_8 = (0x25,)
	_9 = (0x26,)
	_0 = (0x27,)

	ENTER = (0x28,)
	ESC = (0x29,)
	BACKSPACE = (0x2a,)
	TAB = (0x2b,)
	SPACE = (0x2c,)

	ACUTE = (0x2d,)
	PLUS = (0x2e,)
	Å = (0x2f,)
	DIARESIS = (0x30,)
	APOSTROPHE = (0x31,)
	Ä = (0x33,)
	Ö = (0x34,)
	PARAGRAPH = (0x35,)
	COMMA = (0x36,)
	PERIOD = (0x37,)
	MINUS = (0x38,)
	LESS = (0x64,)

	LEFT_CTRL = (0xe0,)
	LEFT_SHIFT = (0xe1,)
	ALT = (0xe2,)
	WINDOWS = (0xe3,)
	RIGHT_CTRL = (0xe4,)
	RIGHT_SHIFT = (0xe5,)
	ALT_GR = (0xe6,)
	MENU = (0xe7,)

	CAPS_LOCK = (0x39,)

	ARROWS = range(0x4f, 0x52)

	# EURO = alt(E)
	# MU = alt(M)

	# EXCL = shift(_1)
	# QUOTE = shift(_2)
	# AT = alt(_2)
	# HASH = shift(_3)
	# POUND = alt(_3)
	# CURRENCY = shift(_4)
	# DOLLAR = alt(_4)
	# PERCENT = shift(_5)
	# AND = shift(_6)
	# SLASH = shift(_7)
	# LBRACE = alt(_7)
	# LPAREN = shift(_8)
	# LSQ = alt(_8)
	# RPAREN = shift(_9)
	# RSQ = alt(_9)
	# EQ = shift(_0)
	# RBRACE = alt(_0)

	# GRAVE = shift(ACUTE)
	# QUESTION = shift(PLUS)
	# BACKSLASH = alt(PLUS)
	# CIRCUMFLEX = shift(DIARESIS)
	# TILDE = alt(DIARESIS)
	# ASTERISK = shift(APOSTROPHE)
	# SEMI = shift(COMMA)
	# COLON = shift(PERIOD)
	# UNDERSCORE = shift(MINUS)
	# GREATER = shift(LESS)
	# BAR = alt(LESS)