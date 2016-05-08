#!/usr/bin/env python3
import random

class PolybiusSquare:
	'''Represents a polybius square, used in ciphers such as ADFGVX.'''

	def __init__(self, sqr_values=[], x_values=[], y_values=[], square={}):
		'''intialises the square, either creating or generating one.
		x_values and y_values must be hashable as they will be dictionary keys.
		:param sqr_values: the values used to create the square
		:param x_values: values used along x-axis when creating square
		:param y_values: values used along the y-axis when creating square
		:param square: dict of values from a polybius square, if provided a polybius
					   square will not be generated these values will be used instead'''			   
		self.sqr_values = sqr_values
		self.x_values = x_values
		self.y_values = y_values
		self.square = square

	def create_square(self, reverse=0):
		'''creates a polybus square using values to init, only works if values have been set in init
		:param reverse: instead of the square values be the key in the dict, the x-y pair will be the key in the
		dict.'''
		if len(self.sqr_values) != (len(self.x_values) * len(self.y_values)):
			raise PolybiusValuesError("There's an invalid ammount of sqr_values, there should be {} not {}".format(len(self.x_values) * len(self.y_values), len(self.sqr_values)))

		x_length = len(self.x_values)
		#self.square = random.randint(0, 10)
		#return None

		for i in range(x_length, len(self.sqr_values) + 1, x_length):
			row_numb = int(i / x_length) - 1
			row = {}
			for x in range(i - x_length, i):
				col_numb = x % x_length
				if not reverse:
					row[self.sqr_values[x]] = str(self.x_values[row_numb]) + str(self.y_values[col_numb])
					#self.square[self.sqr_values[x]] = str(self.x_values[row_numb]) + str(self.y_values[col_numb])
				else:
					row[str(self.x_values[row_numb]) + str(self.y_values[col_numb])] = self.sqr_values[x]
					#self.square[str(self.x_values[row_numb]) + str(self.y_values[col_numb])] = self.sqr_values[x]
			self.square.update(row)

	def valid_square(self, values, square):
		'''checks that the values in the arugement passed are represented in the polybius square
		:param values: list of values to check
		:param square: dict of poly square values to check'''
		not_in = [x for x in values if not square.get(x, 0)]

		if len(not_in) != 0:
			raise PolybiusValuesError("The following values are represented in the square: {}".join(not_in))

class PolybiusValuesError(Exception):
	pass

if __name__ == '__main__':
	values = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
	axiss = list("ADFGVX")
	s = PolybiusSquare(sqr_values=values, x_values=axiss, y_values=axiss)

	#checking each value has been reprsemnted in the square
	print(not len([x for x in values if not s.square.get(x, 0)]))

	#checking valid_square works
	PolybiusSquare().valid_square(list("/"), s.square)