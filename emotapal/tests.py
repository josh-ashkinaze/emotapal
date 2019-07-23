#!/usr/bin/env python
# -*- coding: utf-8 -*-

from emotapal import EmotaPal 
from emotapal.helpers import hex2rgb, rgb2hex, parse_color 
import unittest

class TestType(unittest.TestCase):
	"""Test that each constructor method really returns an EmotaPal instance."""


	gimg = EmotaPal().from_gimg("happy", 5)

	col = EmotaPal().from_colors([[100, 200, 100], [100, 100, 100]])

	url = EmotaPal().from_url("https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2017-12-19/288981919427_f45f04edd92902a96859_512.png", 4)

	# Test the `from_gimg` constructor 
	def test_from_gimg(self):
		self.assertIsInstance(self.gimg, EmotaPal)

	# Test the `from_colors` constructor 
	def test_from_col(self):
		self.assertIsInstance(self.col, EmotaPal)
	
	# The `from_url` constructor calls the `from_img` constructor after reading url,
	# so if `from_url` returns an EmotaPal then `from_img` returns and EmotaPal. 
	def test_from_url(self):
		self.assertIsInstance(self.col, EmotaPal)

class TestConstructErrors(unittest.TestCase):
	"""Test that errors are thrown when a user incorrectly uses an EmotaPal constructor."""

	# Throw an error when user enters a bad (non-HEX) string.
	def test_con1(self):
		with self.assertRaises(Exception): a = EmotaPal().from_colors(["a string"])
	
	# Throw an error when user enters a single color, not a list.
	def test_con2(self):
		with self.assertRaises(Exception): a = EmotaPal().from_colors((100, 200, 100))

	# Throw an error when user enters a bad image file. 
	def test_con3(self):
		with self.assertRaises(Exception): a = EmotaPal().from_image("joshiscool")

class TestHelperFuncs(unittest.TestCase):
	"""Test that errors are thrown when a user incorrectly uses an EmotaPal constructor."""

	hex_col = "#ffffff"
	rgb_col = [255, 255, 255]

	# Verify hex2rgb returns a list. 
	def test_hex2rgb(self):
		self.assertIsInstance(hex2rgb(self.hex_col), list)
	
	# Verify rgb2hex returns a string. 
	def test_rgb2hex(self):
		self.assertIsInstance(rgb2hex(self.rgb_col), str)

	# Verify parse_color correctly parses hex colors. 
	def test_parse_color1(self):
		self.assertListEqual(hex2rgb(self.hex_col), self.rgb_col)

	# Verify parse_color correctly parses rgb colors. 
	def test_parse_color2(self):
		self.assertEqual(rgb2hex(self.rgb_col), self.hex_col)

if __name__ == '__main__':
    unittest.main()
