#!/usr/bin/env python3
import ciphers
import os

class ROT13(ciphers.MonoalphabeticSubCipher):
	def __init__(self, plaintext="", ciphertext=""):
		super().__init__(plaintext, ciphertext)
		if self._valid_values([plaintext, ciphertext], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the plaintext or ciphertext has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		self.shift = 13

if __name__ == '__main__':
	c = ROT13("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	c.encrypt()
	print(c.ciphertext)