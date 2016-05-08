#!/usr/bin/env python3

class Cipher:
	def __init__(self, plaintext="", ciphertext=""):
		self.plaintext = plaintext.replace(" ", "").upper()
		self.ciphertext = ciphertext
		#default legal chars is upper case alph
		self._legal_chars = [chr(x) for x in range(65, 91)]

		#maps A-Z, no numb values, so a = 0, b = 1...z = 25 etc.
		self.char_map = {x:ord(x) - 65 for x in self._legal_chars}
		self.reverse_char_map = {self.char_map[x]:x for x in self.char_map}

	def encrypt(self):
		pass

	def decrypt(self):
		pass

	def _valid_values(self, values, legal_values):
		'''checks that only valid chars are used in a str
		:param value: list of values to check
		:param legal_values: list of valid values'''
		#errors = [x for i in values for x in i if str(self._legal_chars).find(x) == -1]
		errors = [x for i in values for x in i if "".join(legal_values).find(x) == -1]

		if errors: return 1
		else: return 0

class TranspositionCipher(Cipher):
	def __init__(self, plaintext, ciphertext, polybius_sqr={}):
		super().__init__(plaintext, ciphertext)
		self.polybius_sqr = polybius_sqr

	def _create_square(self, x_values=[], y_values=[], sqr_values=[]):
		'''creates polybius square using values provided'''
		sqr = polybius.PolybiusSquare(sqr_values=sqr_values, x_values=x_values, y_values=y_values)
		sqr.create_square()
		self.polybius_sqr = sqr.square

class MonoalphabeticSubCipher(Cipher):
	'''The collective data and behaviour of substituions ciphers that use shifts,
	i.e caesars, ROT13, Atbash etc.'''
	def __init__(self, plaintext="", ciphertext="", shift=0):
		super().__init__(plaintext, ciphertext)
		self.shift = shift

		#the following allows the functions to be changed in the atbash cipher without having
		#to change the method.
		#the forumlas used for encryption and decryption, x is the char and s is the shift
		self.get_e = lambda x, s: self.reverse_char_map[(self.char_map[x] + s) % 26]
		self.get_d = lambda x, s: self.reverse_char_map[(self.char_map[x] - s) % 26]

	def encrypt(self):
		'''encrypts using the forumla E(x) = (x + n) mod 26'''
		self.ciphertext = "".join([self.get_e(x, self.shift) for x in self.plaintext])
		return self.ciphertext

	def decrypt(self):
		'''decrypts using the forumla D(x) = (x - n) mod 26'''
		self.plaintext = "".join([self.get_d(x, self.shift) for x in self.ciphertext])
		return self.plaintext

class IllegalCharsError(Exception):
	pass

class InvalidKeyError(Exception):
	pass

class CiphertextError(Exception):
	pass

class PolybiusSquareError(Exception):
	pass