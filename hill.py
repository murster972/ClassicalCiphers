#!/usr/bin/env python3
import ciphers
import matrix
import fractions
import os

class Hill(ciphers.Cipher):
	def __init__(self, plaintext="", key=[], ciphertext=""):
		super().__init__(plaintext, ciphertext)
		key_values = [self.char_map[x] for x in key]
		self.key = matrix.Matrix(x=3, y=3, values=key_values)

		if self._valid_values([self.plaintext, self.ciphertext, key], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the plaintext, ciphertext or key has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))
		
		if len(key) != 9:
			raise cipher.InvalidKeyError("The key must be 9 chars long.")

		if fractions.gcd(self.key._get_determinant(), 26) != 1:
			raise ciphers.InvalidKeyError("The key that has been provided is invalid, the determinant of the key must be coprime with 26.")

		#adds padding, by adding the last char again, until len is divisble by three
		if self.plaintext and len(self.plaintext) % 3 != 0:
			self.plaintext = self.plaintext + (self.plaintext[len(self.plaintext) - 1] * (3 - (len(self.plaintext)  % 3)))
		
		if self.ciphertext and len(self.ciphertext) % 3 != 0:
			raise CiphertextError("Invalid ciphertext length, length of ciphertextm must be divisble by 3.")

	def encrypt(self):
		self.ciphertext = ""

		for i in range(3, len(self.plaintext) + 1, 3):
			cur_values = [self.char_map[x] for x in list(self.plaintext[i - 3:i])]
			cur_matrix = matrix.Matrix(x=3, y=1, values=cur_values)
			cipher_matrix = (self.key * cur_matrix) % 26
			cur_ciphertext = [self.reverse_char_map[x] for x in cipher_matrix.values]
			self.ciphertext += "".join(cur_ciphertext)
		return self.ciphertext

	def decrypt(self):
		ajd_k = self.key._get_adjugate()
		inverse_d = self._get_d_inverse(self.key._get_determinant(), 26)
		inverse_k = ajd_k * inverse_d

		self.plaintext = ""

		for i in range(3, len(self.ciphertext) + 1, 3):
			cur_values = [self.char_map[x] for x in list(self.ciphertext[i - 3:i])]
			cur_matrix = matrix.Matrix(x=3, y=1, values=cur_values)
			plain_matrix = (inverse_k * cur_matrix) % 26
			cur_plaintext = [self.reverse_char_map[x] for x in plain_matrix.values]
			self.plaintext += "".join(cur_plaintext)
		return self.plaintext

	def _get_d_inverse(self, a, m):
		'''calculates the inverse of d mod m'''
		#this is an inefficent way of finding the inverse of a, but will work as the values of
		#a and m are small in this scenario.
		#a^-1 is the inverse of a
		#a^-1 is such that: (a^-1 * a) mod m = 1
		inverse = 0

		while (a * inverse) % m != 1 and inverse < m:
			inverse += 1

		return inverse

if __name__ == '__main__':
	os.system("clear")
	h = Hill(plaintext="ATTACKATDAWN", key="CEFJCBDRH")
	#h = Hill(ciphertext="PFOGOANPGXFX", key="CEFJCBDRH")
	h.encrypt()
	print(h.ciphertext)