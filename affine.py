#!/usr/bin/env python3
import ciphers
import fractions
import sys
import os

class Affine(ciphers.Cipher):
	'''reprsenst an instance of the Affine Cipher, which uses A-Z, as it's alph.'''
	def __init__(self, a, b, plaintext="", ciphertext=""):
		'''Intialises values to be used
		:param plaintext: text to be encrypted
		:param ciphertext: text to be decrypted
		:param a: is first part of key and a must be coprime to m, which is 26
		:param b: is second part of key and the shift of the cipher'''
		super().__init__(plaintext)
		self._valid_values(self.plaintext, self._legal_chars)
		#a and m must be coprime, although a being 1 is coprime with m as 26, it makes the cipher weaker
		#since it reduces it to a linear shift, hence it's valid if choosen
		self.a = a
		self.inverse_a = None
		self.b = b
		self.m = 26

		#dict of corrosponding number values for alph, e.g. a = 0, b = 1, etc.
		self.char_map = {x:ord(x) - 65 for x in self._legal_chars}
		self.reverse_char_map = {self.char_map[x]:x for x in self.char_map}
		#finds all coprime values of m
		self._valid_a_values = [x for x in range(2, self.m) if fractions.gcd(x, self.m) == 1]
		self._valid_a_b()

	def encrypt(self):
		'''encrypts using E(x) = (ax + b) mod m'''
		self.ciphertext = ""
		for i in self.plaintext:
			self.ciphertext += self.reverse_char_map[(self.a * self.char_map[i] + self.b) % self.m]

		return self.ciphertext

	def decrypt(self):
		'''decrypts using D(x) = a^-1(x - b) mod m'''
		a_inverse = self._get_a_inverse()
		self.plaintext = ""

		for i in self.ciphertext:
			self.plaintext += self.reverse_char_map[(a_inverse * (self.char_map[i] - self.b)) % self.m]

		return self.plaintext

	def _get_a_inverse(self):
		'''calculates the inverse of a mod m'''
		#this is an inefficent way of finding the inverse of a, but will work as the values of
		#a and m are small in this scenario.
		#a^-1 is the inverse of a
		#a^-1 is such that: (a^-1 * a) mod m = 1
		inverse = 0

		while (self.a * inverse) % self.m != 1 and inverse < self.m:
			inverse += 1

		return inverse

	def _valid_a_b(self):
		'''checks that a and b are valid values'''
		a_valid = [1 for x in self._valid_a_values if self.a == x]
		b_valid = 1 if type(self.b) is int and self.b > 0 else 0

		if not a_valid or not b_valid:
			raise Illegal_a_b_ValueError("The values passed for a/b are invalid.\nb must be greater than 0 and an integer and a must be corpime to {} and but not equal 1.".format(self.m))

class Illegal_a_b_ValueError(Exception):
	pass

if __name__ == '__main__':
	os.system("clear")
	a = Affine(5, 9, plaintext="AFFINECIPHER")
	a.encrypt()
	a.decrypt()
	print(a.ciphertext)