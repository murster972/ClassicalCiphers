#!/usr/bin/env python3
import ciphers
import random
import os

class OneTime(ciphers.Cipher):
	def __init__(self, plaintext="", ciphertext="", key=""):
		super().__init__(plaintext, ciphertext)
		#key must be at least as long as plaintext
		self.key = key.upper()

		if self._valid_values([self.plaintext, self.ciphertext, self.key], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the plaintext, ciphertext or key has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		if self.key and (len(self.key) < len(self.plaintext) or len(self.key) < len(self.ciphertext)):
			raise ciphers.InvalidKeyError("The key cannot be shorter than the plaintext.")
		elif not self.key:
			self._gen_key()

	def encrypt(self):
		'''encrypts using, E = msg + key mod 26'''
		self.ciphertext = ""

		for i in range(len(self.plaintext)):
			msg_key = self.char_map[self.plaintext[i]] + self.char_map[self.key[i]]
			self.ciphertext += self.reverse_char_map[msg_key % 26]
		return self.ciphertext

	def decrypt(self):
		'''decrypts using D = cipher - key mod 26'''
		self.plaintext = ""

		for i in range(len(self.ciphertext)):
			cipher_key = self.char_map[self.ciphertext[i]] - self.char_map[self.key[i]]
			self.plaintext += self.reverse_char_map[cipher_key % 26]
		return self.plaintext

	def _gen_key(self):
		rand_key = [self._legal_chars[random.randint(0, len(self._legal_chars) - 1)] for x in range(len(self.plaintext))]
		self.key = "".join(rand_key)

if __name__ == '__main__':
	o = OneTime(ciphertext="EQNVZ", key="XMCKL")
	o.decrypt()
	print(o.plaintext)