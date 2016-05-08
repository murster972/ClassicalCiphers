#!/usr/bin/env python3
from random import shuffle
import polybius
import ciphers
import os
import sys

class ADFGVX(ciphers.Cipher):
	'''reprsents an instance of the ADFGVX Cipher'''
	def __init__(self, plaintext="", ciphertext="", key="", polybius_sqr={}):
		'''Intialsies varibales and creates a grid to use in encryption
		:param plaintext: message to encrypt
		:param key: key to use in encryption and decryption
		:param polybius_sqr: polybius_square used in encryption and decryption, optional, and 
							will be randomly generated if not provided.'''
		super().__init__(plaintext, ciphertext)
		self.key = key.upper()
		#extends legal chars to include the chars, 0 - 9
		self._legal_chars.extend([str(x) for x in range(0, 10)])

		#checks that plaintext, ciphertext and key are legal
		if self._valid_values([self.plaintext, self.key, self.ciphertext], self._legal_chars):
			raise ciphers.IllegalCharsError("Either the key, plaintext or ciphertext has illegal chars.\nLegal chars: {}".format("".join(self._legal_chars)))

		#checks if polybius square is provided, if so checks it's legal
		if polybius_sqr:
			#doesnt check if values arre reprsented using ADFGVX
			polybius.PolybiusSquare().valid_square(self._legal_chars, polybius_sqr)
			self.polybius_sqr = polybius_sqr
		else:
			self.polybius_sqr = {}
			self._create_polybius_sqr()

	def encrypt(self):
		'''encrypts self.plaintext using ADFGX cipher'''
		fractioned_msg = "".join([self.polybius_sqr[x] for x in self.plaintext])
		no_rows = int(len(fractioned_msg) / len(self.key))
		row_len = len(self.key)
		rows = []
		self.ciphertext = ""
		
		#put fractioned msg into rows rows under key
		for i in range(row_len, len(fractioned_msg), row_len):
			rows.append(fractioned_msg[i - row_len: i])

		#adds anything reamining
		if i != len(fractioned_msg): rows.append(fractioned_msg[i: len(fractioned_msg)])

		#sort rows int cols
		cols = []

		for i in range(row_len):
			cols.append("".join([x[i] for x in rows if len(x) - 1 >= i]))

		#creates a list of key indexes, so that when sorted by alph, the col of two letters that are the same can be determined
		key_indexes = self._get_key_indexes(self.key)

		#puts cols in order based on key in alph order
		for x in key_indexes:
			self.ciphertext += cols[x[1]] + " "

		return self.ciphertext

	def decrypt(self):
		'''decrypts ciphertext using ADFGVX'''
		#split into colums
		cols = self.ciphertext.split(" ")
		key_indexes = self._get_key_indexes(self.key)
		key_sorted = list(self.key)
		key_sorted.sort()
		sorted_key_indexes = [(key_sorted[x], x) for x in range(len(key_sorted))]
		original_cols = {}
		j = 0

		try:
			for i in sorted_key_indexes:
				for j in range(len(key_indexes)):
					if key_indexes[j][0] == i[0]:
						original_cols[key_indexes[j][1]] = cols[i[1]]
						key_indexes.pop(j)
						break

		except (KeyError, IndexError) as e:
			print("The following error occured while sorting into cols, please ensure the correct key is being used: {}".format(e))
			sys.exit(1)

		original_cols = [original_cols[x] for x in original_cols]
		no_rows = max([len(x) for x in original_cols])
		char_stream = ""

		#goes through each row, turning square into stream of chars
		for x in range(no_rows):
			for y in range(len(self.key)):
				char_stream += "" if len(original_cols[y]) <= x else original_cols[y][x]

		#reverse polybius_sqaure so cipher values go to plaintext value
		polybius_sqaure = {self.polybius_sqr[x]:x for x in self.polybius_sqr}
		self.plaintext = ""

		#gets pairs from stream of chars and matches each pair to plaintext value
		for i in range(2, len(char_stream) + 2, 2):
			self.plaintext += polybius_sqaure[char_stream[i - 2:i]]

		return self.plaintext

	def _get_key_indexes(self, key):
		'''returns an array of tuples - in alph order - with a each letter in a key paired with it's index,
		so that keys that have the same letters multiple times can be sorted alph and still have
		the correct columns.
		:param key: key to get indexes of'''
		key_indexes = [(key[x], x) for x in range(len(key))]
		key_indexes.sort()
		return key_indexes

	def _create_polybius_sqr(self):
		'''creates 6x6 Polybius square with mixed alph, A-Z, 0-9'''
		mixed_alph = [chr(x) for x in range(65, 91)]
		mixed_alph.extend([str(x) for x in range(0, 10)])
		shuffle(mixed_alph)
		x_y_axis = "ADFGVX"
		sqr = polybius.PolybiusSquare(sqr_values=mixed_alph, x_values=x_y_axis, y_values=x_y_axis)
		sqr.create_square()
		self.polybius_sqr = sqr.square

def main():
	os.system("clear")
	#cipher = test.encrypt(test.plaintext, test.key, test.grid)
	"""grid = {'V': 'XF', 'I': 'FX', 'G': 'AD', 'J': 'XG', 'Y': 'FG', '8': 'AF', '0': 'GV', 'O': 'DG', 'T': 'GA', 'D': 'XV', 'W': 'VG', '7': 'XX', 'E': 'GX', 'L': 'DF', 'U': 'AV', 'Q': 'DD', '6': 'XA', '4': 'VA', 'R': 'VD', 'X': 'GF', 'C': 'VF', 'M': 'DV', 'B': 'GD', '9': 'FD', '5': 'AG', 'N': 'VX', 'F': 'GG', 'Z': 'XD', '2': 'FA', 'P': 'AX', '1': 'DX', 'H': 'VV', 'S': 'DA', 'K': 'FV', '3': 'FF', 'A': 'AA'}
	ciphertext = "ADA ADD DXA GVA GADX XGA GAG"
	key = "testkey"
	test = ADFGVX(key=key, polybius_sqr=grid, ciphertext=ciphertext)
	test.decrypt()
	print(test.plaintext)"""

	test2 = ADFGVX(plaintext="test\message", key="testkey")
	test2.encrypt()
	test2.decrypt()
	print(test2.plaintext)

if __name__ == '__main__':
	main()