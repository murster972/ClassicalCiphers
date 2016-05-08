#!/usr/bin/env python3
import polybius
import ciphers
import random
import os

class Bifid(ciphers.Cipher):
	def __init__(self, plaintext="", ciphertext="", sqr={}):
		plaintext = plaintext.replace("J", "I")
		super().__init__(plaintext, ciphertext)
		
		self._legal_chars.pop(self._legal_chars.index("J"))

		if self._valid_values([plaintext.replace("J", "I"), ciphertext], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the plaintext or ciphertext has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		if sqr:
			#validate square values
			polybius.PolybiusSquare().valid_square(self._legal_chars, sqr)
			self.polybius_sqr = sqr
			self.reverse_poly_sqr = {self.polybius_sqr[x]:x for x in self.polybius_sqr}
		else:
			self.polybius_sqr = {}
			self.reverse_poly_sqr = {}
			self._create_poly_sqr()

	def encrypt(self):
		coord_rows = [(self.polybius_sqr[x][0], self.polybius_sqr[x][1]) for x in self.plaintext]
		coord_stream = [x[0] for x in coord_rows]
		coord_stream.extend([x[1] for x in coord_rows])
		coord_stream = "".join(coord_stream)

		self.ciphertext = ""

		for i in range(2, len(coord_stream) + 1, 2):
			self.ciphertext += self.reverse_poly_sqr[coord_stream[i - 2:i]]

		return self.ciphertext

	def decrypt(self):
		coord_stream = [self.polybius_sqr[x] for x in self.ciphertext]
		coord_row_1 = "".join(coord_stream[:int(len(coord_stream) / 2)])
		coord_row_2 = "".join(coord_stream[int(len(coord_stream) / 2):])
		
		self.plaintext = ""

		for i in range(len(coord_row_1)):
			self.plaintext += self.reverse_poly_sqr[coord_row_1[i] + coord_row_2[i]]

		return self.plaintext

	def _create_poly_sqr(self):
		'''creates polybius square used in bifid, cipher, uses a-z, but i/j are the same,
		and uses 1-5 for x and y axis'''
		sqr_values = [chr(x) for x in range(65, 91) if chr(x) != 'J']
		random.shuffle(sqr_values)
		axis = [x for x in range(1, 6)]
		sqr = polybius.PolybiusSquare(sqr_values=sqr_values, x_values=axis, y_values=axis)
		sqr.create_square()
		self.polybius_sqr = sqr.square
		self.reverse_poly_sqr = {self.polybius_sqr[x]:x for x in self.polybius_sqr}

if __name__ == '__main__':
	os.system("clear")
	b = Bifid(ciphertext="SEQMIFESUH", sqr={'H': '42', 'K': '34', 'X': '53', 'W': '31', 'F': '11', 'I': '52', 'U': '13', 'L': '51', 'R': '12', 'P': '14', 'D': '32', 'Y': '23', 'G': '35', 'C': '54', 'N': '33', 'B': '25', 'A': '21', 'Q': '24', 'E': '22', 'V': '44', 'M': '43', 'O': '41', 'S': '15', 'T': '45', 'Z': '55'})
	b.decrypt()
	print(b.polybius_sqr)
	print(b.plaintext)