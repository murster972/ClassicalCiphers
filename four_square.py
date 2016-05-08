#!/usr/bin/env python3
import ciphers
import polybius
import os

class FourSquare(ciphers.Cipher):
	def __init__(self, key1, key2,  plaintext="", ciphertext=""):
		plaintext = plaintext.replace("J", "I")
		super().__init__(plaintext, ciphertext)
		
		self._legal_chars.pop(self._legal_chars.index("J"))

		if self._valid_values([self.plaintext, self.ciphertext, key1, key2], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the plaintext or ciphertext has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		#key1 used in top right square, key2 bottom left square
		self.key1 = key1
		self.key2 = key2
		
		self.ciphertext_squares = []
		self.plaintext_square = []
		self.plaintext_square_reverse = []
		self._create_squares()
		self._reverse_ciphertext_squares()

	def encrypt(self):
		#repeates last char of plaintext if not an even length
		self.plaintext += self.plaintext[len(self.plaintext) - 1] if len(self.plaintext) % 2 != 0 else ""
		self.ciphertext = ""

		for i in range(2, len(self.plaintext) + 1, 2):
			pair = self.plaintext[i - 2:i]
			pair = [self.plaintext_square[pair[0]], self.plaintext_square[pair[1]]]
			cipher_pair = [str(pair[0][0]) + str(pair[1][1]), str(pair[1][0]) + str(pair[0][1])]
			cipher_pair = self.ciphertext_squares_reverse[0][cipher_pair[0]] + self.ciphertext_squares_reverse[1][cipher_pair[1]]
			self.ciphertext += cipher_pair
		return self.ciphertext

	def decrypt(self):
		self.ciphertext += self.ciphertext[len(self.ciphertext) - 1] if len(self.ciphertext) % 2 != 0 else ""
		self.plaintext = ""

		for i in range(2, len(self.ciphertext) + 1, 2):
			cipher_pair = self.ciphertext[i - 2: i]
			cipher_pair = [self.ciphertext_squares[0][cipher_pair[0]], self.ciphertext_squares[1][cipher_pair[1]]]
			pair = [str(cipher_pair[0][0]) + str(cipher_pair[1][1]), str(cipher_pair[1][0]) + str(cipher_pair[0][1])]
			pair = self.plaintext_square_reverse[pair[0]] + self.plaintext_square_reverse[pair[1]]
			self.plaintext += pair
		return self.plaintext

	def _reverse_ciphertext_squares(self):
		self.ciphertext_squares_reverse = [{}, {}]

		for i in self.ciphertext_squares[0]:
			self.ciphertext_squares_reverse[0][self.ciphertext_squares[0][i]] = i
		for i in self.ciphertext_squares[1]:
			self.ciphertext_squares_reverse[1][self.ciphertext_squares[1][i]] = i

	def _create_squares(self):
		'''creates four 5x5 squares, one plaintext, two ciphertext,
		although two plaintext are used in FourSquare one will be suffice.'''
		'''creates four 5x5 squares, one plaintext, two ciphertext,
		although two plaintext are used in FourSquare one will be suffice.'''
		#creates plaintext sqaure
		axis = [x for x in range(5)]
		sqr = polybius.PolybiusSquare(x_values=axis, y_values=axis, sqr_values=self._legal_chars)
		sqr.create_square()
		self.plaintext_square = sqr.square
		self.plaintext_square_reverse = {self.plaintext_square[x]:x for x in self.plaintext_square}

		#exits method if ciphertext squares have been provided
		if self.ciphertext_squares: return None

		sqr_values_1 = list(self.key1)
		sqr_values_1.extend(self._legal_chars)
		sqr_values_1 = self._remove_duplicates(sqr_values_1)

		sqr_values_2 = list(self.key2)
		sqr_values_2.extend(self._legal_chars)
		sqr_values_2 = self._remove_duplicates(sqr_values_2)

		#if empty dict isnt passed for square, it fucks up - don't know why, yet - as the instance varibale
		#'square' acts like a class variable or like its static when the method create_square is called
		#it changes the value of the instance variable for every instance of the class PolybiusSquare.
		sqr1 = polybius.PolybiusSquare(x_values=axis, y_values=axis, sqr_values=sqr_values_1, square={})
		sqr1.create_square()
		self.ciphertext_squares.append(sqr1.square)
		sqr2 = polybius.PolybiusSquare(x_values=axis, y_values=axis, sqr_values=sqr_values_2, square={})
		sqr2.create_square()
		self.ciphertext_squares.append(sqr2.square)

	def _remove_duplicates(self, x):
		'''returns a list with any duplicates removed'''
		in_list = []
		no_dupls = []

		for i in range(len(x)):
			try:
				if no_dupls.index(x[i]):
					pass
			except ValueError:
				no_dupls.append(x[i])
				in_list.append(x[i])

		return no_dupls

if __name__ == '__main__':
	os.system("clear")
	f = FourSquare("EXAMPLE", "KEYWORD", ciphertext="TWSP")
	#f.encrypt()
	f.decrypt()
	print(f.plaintext)