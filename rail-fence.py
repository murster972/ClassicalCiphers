#!/usr/bin/env python3
import ciphers
import os

class RailFence(ciphers.Cipher):
	def __init__(self, no_rails=1, plaintext="", ciphertext=""):
		super().__init__(plaintext, ciphertext)
		self.no_rails = no_rails

	def encrypt(self):
		rails = [[] for x in range(self.no_rails)]
		cur_rail = 1
		down = 1

		for i in self.plaintext:
			if cur_rail == self.no_rails: down = 0
			elif cur_rail == 1 and not down: down = 1
			rails[cur_rail - 1].append(i)
			cur_rail -= -1 if down else 1

		#adds a space to the end of each rail(bar last)
		for i in range(self.no_rails - 1): rails[i].append(" ")

		self.ciphertext = "".join([j for x in rails for j in x])

	def decrypt(self):
		rails = [[] for x in range(self.no_rails)]
		tmp = [self.plaintext, self.ciphertext]
		self.plaintext = self.ciphertext
		self.encrypt()
		c = self.ciphertext
		self.plaintext = tmp[0]
		self.ciphertext = tmp[1]

		spaced = ""
		j = 0

		for i in range(len(c)):
			if c[i] == " ": spaced += " "
			else:
				spaced += self.ciphertext[j]
				j += 1

		rails = [[x] for x in spaced.split(" ")]
		rails_index = [0 for x in range(self.no_rails)]
		cur_rail = 1
		down = 1
		self.plaintext = ""

		while True:
			try:
				if cur_rail == self.no_rails: down = 0
				elif cur_rail == 1 and not down: down = 1
				index = rails_index[cur_rail - 1]
				self.plaintext += "".join(rails[cur_rail - 1])[index]
				rails_index[cur_rail - 1] += 1
				cur_rail -= -1 if down else 1
			except IndexError:
				break

if __name__ == '__main__':
	os.system("clear")
	r = RailFence(no_rails=5, ciphertext="WCLEESOFECAIVDENRDEEAOERT")
	r.decrypt()
	print(r.plaintext)