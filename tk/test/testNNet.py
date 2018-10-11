#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import sys
sys.path.append('..')

import numpy as np
from tk.TKGame import TKGame
from tk.keras.NNet import NNetWrapper as NNet
from tk.test.testTKLogick import generate_encoded_state


class TestNNet(unittest.TestCase): #TODO: rename to testTKLogick
	def setUp(self):
		self.g = TKGame()
		self.n1 = NNet(self.g)
		self.n1.load_checkpoint('temp/','best.pth.tar')
		self.n1.nnet.model._make_predict_function()

	def tearDown(self):
		self.g = None
		self.n1 = None


	def testNNOutputs(self):
		state = [9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, None, None]
		encoded_state = generate_encoded_state(state)
		canonical_form = self.g.getCanonicalForm(encoded_state, -1)

		prediction = self.n1.predict(canonical_form)
		action = np.argmax(prediction[0])

		# print(canonical_form)
		# print(prediction)

		self.assertEqual(action,10)


if __name__ == '__main__':
    unittest.main()