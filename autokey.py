#!/usr/bin/env python3
import ciphers
import polybius
import os

class Autokey(ciphers.Cipher):
	'''Reperesents an instance of the Autokey Cipher, but uses polybius square instead of tabula recta'''
	def __init__(self, plaintext="", key="", ciphertext=""):
		super().__init__(plaintext, ciphertext)
		self.key = key.upper()

		if self._valid_values([self.plaintext, self.ciphertext, self.key], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the key, plaintext or ciphertext has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		#char map, a = 0, b = 1, etc...
		self.char_map = {x:ord(x) - 65 for x in self._legal_chars}
		self.reverse_char_map = {self.char_map[x]:x for x in self.char_map}

		self.polybius_sqr = {}
		self._create_polybius_sqaure()

	def encrypt(self):
		if len(self.key) > len(self.plaintext):
			raise InvalidKeyError("Key cannot be longer than plaintext.")
		keystream = self.key
		i = len(self.key)

		while i < len(self.plaintext):
			for x in self.plaintext:
				if i > len(self.plaintext) - 1: break
				keystream += x
				i += 1

		self.ciphertext = ""
		for i in range(len(self.plaintext)):
			self.ciphertext += self.polybius_sqr[self.plaintext[i] + keystream[i]]
		return self.ciphertext

	def decrypt(self):
		pass

	def _create_polybius_sqaure(self):
		axis_values = self._legal_chars
		sqr_values = self._gen_square_values()
		sqr = polybius.PolybiusSquare(x_values=axis_values, y_values=axis_values, sqr_values=sqr_values)
		sqr.create_square(reverse=1)
		self.polybius_sqr = sqr.square

	def _gen_square_values(self):
		'''gens square values to be used in polybius square for autokey, returns list of alph, shifted
		to left by 0 to 25'''
		sqr_values = []
		for i in range(0, 26):
			sqr_values.extend(self._shift_alph(i))
		return sqr_values

	def _shift_alph(self, shift):
		'''returns the alph, shifted to the left by the value passed
		:param shift: shift value'''
		alph = []
		for x in self._legal_chars:
			e = (self.char_map[x] + shift) % 26
			alph += self.reverse_char_map[e]
		return alph

if __name__ == '__main__':
	os.system("clear")
	a = Autokey(plaintext="meetmeatthecorner", key="king")
	a.encrypt()
	print(a.ciphertext)