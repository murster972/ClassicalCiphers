#!/usr/bin/env python3
import ciphers
import os

class Caesars(ciphers.MonoalphabeticSubCipher):
	def __init__(self, plaintext="", ciphertext=""):
		super().__init__(plaintext, ciphertext)
		if self._valid_values([plaintext, ciphertext], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the plaintext or ciphertext has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		self.shift = 23