#!/usr/bin/env python3
import ciphers
import os

class Atbash(ciphers.MonoalphabeticSubCipher):
	'''Reperesents an instance of the Atbash cipher,
	uses the function E(x) = (26 - x) mod 26 + 1, to encrypt and decrypt'''
	def __init__(self, plaintext="", ciphertext=""):
		super().__init__(plaintext, ciphertext)

		if self._valid_values([plaintext, ciphertext], self._legal_chars):
			raise ciphers.IllegalCharsError("The values for plaintext/ciphertext have illegal chars.\nThe following are legal chars: {}".format("".join(self._legal_chars)))

		#changes char map from a = 0, b = 1...z = 25 to a = 1, b = 2...z = 26
		self.char_map = {x:ord(x) - 64 for x in self._legal_chars}
		self.reverse_char_map = {self.char_map[x]:x for x in self.char_map}

		#change encryption and decryption to the same functions, to atbash formula
		self.get_e_d = lambda x: self.reverse_char_map[(26 - self.char_map[x]) % 26 + 1]

	def encrypt(self):
		'''encrypts using atbash cipher, E(x) = (26 - x) mod 26 + 1'''
		self.ciphertext = "".join([self.get_e_d(x) for x in self.plaintext])
		return self.ciphertext

	def decrypt(self):
		'''decrypts using atbash cipher, E(x) = (26 - x) mod 26 + 1'''
		self.plaintext = "".join([self.get_e_d(x) for x in self.ciphertext])
		return self.plaintext

if __name__ == '__main__':
	os.system("clear")
	a = Atbash(plaintext="ABCEDFGHIJKLMNOPQRSTUVWXYZ")
	a.encrypt()
	print(a.ciphertext)