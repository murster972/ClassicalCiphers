#!/usr/bin/env python3
#-*- coding: utf-8 -*-
class Matrix:
	'''represents a matrix of 1x1, 1x3, 3x3 and 3x1'''
	def __init__(self, values, x, y):
		'''intialises values and checks if valid
		:param values: values of the matrix
		:param x: x size of matrix(number of rows), i.e 3x1 matrix x = 3
		:param y: y size of matrix(number of cols), i.e 3x1 matrix y = 1'''
		#TODO: ensure values are valid
		self.values = values
		self.x = x
		self.y = y
		self.rows = self._get_rows()

		if (self.x != 1 and self.x != 3) or (self.y != 1 and self.y != 3):
			raise MatrixSizeError("Only 1x1, 1x3, 3x3 and 3x1 matrices can be represented.")

		#checks that the values passed fit the size of the matrix
		invalid_row_len = [x for x in self.rows if len(x) != self.y]
		if invalid_row_len or len(self.rows) != self.x or len(self.values) != (self.x * self.y):
			raise MatrixValueError("The values of the arguments 'x, y and values' are incorrect, please check them.")

	def __mul__(self, m):
		'''returns the result of an instance of a matrix mutlipled an integer or a 3x3 * 1x1 matrix'''
		if not isinstance(m, Matrix) and isinstance(m, int):
			new_vals = [x * m for x in self.values]
			return Matrix(values=new_vals, x=3, y=3)
		elif not isinstance(m, Matrix):
			raise MatrixMultiplyError("You can only multipy a matrix by another martix or by an integer.")
		
		#if (self.x != 3 or self.y != 3) or (m.x != 1 or m.y != 1):
		#	raise MatrixMultiplyError("You can only mutliply 3x3 by a 1x1 matrix.")

		if self.y != m.x:
			raise MatrixMultiplyError("To multipy to matrix a by matrix b a.y must equal a.x.")

		#quick fix so only works with 3x3 * 1x1
		m_x = 0
		new_values = []

		for i in self.rows:
			cur_new_value = 0
			for j in i:
				cur_new_value += m.rows[m_x][0] * j
				m_x += 1
			new_values.append(cur_new_value)
			m_x = 0
		return Matrix(x=3, y=1, values=new_values)

	def __mod__(self, m):
		'''returns an new matrix with the values of the current matrix mod m'''
		if not isinstance(m, int):
			raise MatrixModularError("You can only mod a matrix by an integer.")

		values = [x % m for x in self.values]
		return Matrix(values, self.x, self.y)

	def _get_determinant(self):
		'''
		currently only works with 3x3 matrix
		det(A)=A00(A11*A22−A12*A21)−A01(A10*A22−A12*A20)+A02(A10*A21−A11*A20)
		A = [A00 A01 A02
			 A10 A11 A12
			 A20 A21 A22]
		'''
		if self.x != 3 or self.y != 3:
			raise MatrixSizeError("The determinant can currently only be found for a 3x3  matrix.")

		rows = self._get_rows()
		determ = rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
		determ -= rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
		determ += rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
		return determ

	def _get_adjugate(self):
		cofactors = self._get_cofactors()
		new_vals = []
		new_vals.extend([cofactors.rows[0][0], cofactors.rows[1][0], cofactors.rows[2][0]])
		new_vals.extend([cofactors.rows[0][1], cofactors.rows[1][1], cofactors.rows[2][1]])
		new_vals.extend([cofactors.rows[0][2], cofactors.rows[1][2], cofactors.rows[2][2]])
		return Matrix(values=new_vals, x=3, y=3)

	def _get_cofactors(self):
		'''returns the cofactor of a 3x3 matrix'''
		minors = self._get_minors()
		new_values = []

		for i in range(len(minors.rows)):
			for j in range(len(minors.rows[i])):
				if (i + j) % 2 != 0:
					new_values.append(minors.rows[i][j] * -1)
				else:
					new_values.append(minors.rows[i][j])

		return Matrix(values=new_values, x=3, y=3)


	def _get_minors(self):
		'''returns the matrix of minors of a 3x3 matrix'''
		minror_vals = []

		for i in range(len(self.rows)):
			for j in range(len(self.rows[i])):
				cur_vals = self._get_minor_values(i, j)
				determ_val = (cur_vals[0] * cur_vals[3]) - (cur_vals[1] * cur_vals[2])
				minror_vals.append(determ_val)

		return Matrix(values=minror_vals, x=3, y=3)

	def _get_minor_values(self, row, col):
		'''returns the 2x2 matrix that dosent include the col and row values provied of the rows,
		this is 2x2 matrix is then used to calculate the minors'''
		vals = []

		for i in range(len(self.rows)):
			if i == row: continue
			for j in range(len(self.rows[i])):
				if j == col: continue
				vals.append(self.rows[i][j])

		return vals

	def _get_rows(self):
		#rows = [self.values[x - self.y:x] for x in range(self.y, (self.y * self.x) + 1, self.y)]
		rows = []
		for i in range(self.y, (self.y * self.x) + 1, self.y):
			rows.append(self.values[i - self.y:i])
		return rows

class MatrixValueError(Exception):
	pass

class MatrixSizeError(Exception):
	pass

class MatrixMultiplyError(Exception):
	pass

class MatrixModularError(Exception):
	pass