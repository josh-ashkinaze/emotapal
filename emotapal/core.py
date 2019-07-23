#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorthief import ColorThief # grab color info 
from sklearn.externals import joblib # open our classifier
from collections import OrderedDict # find unique list values, maintaining order
import emotapal.helpers as helpers # helper functions 
import seaborn as sns # make color palette
import matplotlib.pyplot as plt # assist with color palette
import os, sys # point to the right places
from afinn import Afinn # compute sentiment

"""
         .        .  
  * _  __|_  _. __|_  
  |(_)_) [ )(_]_) [ )
._|

"""					

class EmotaPal():
	""" 
	An EmotaPal is a palette of words and colors. 
	Just as a 'color palette' describes the colors of some visual object, 
	an 'emotion palette' describes the emotions felt from a visual object. 
	An EmotaPal combines both pieces (visual and psychological) of information. 

	Attributes: 
		topn (int): Return only the topn best color-emotion matches 
		unique_words (bool): Return unique list of words (sometimes a word is matched by >1 colors in a palette)
		_info (list): The actual palette information (emotions, colors, and distance to emotion-color match) as a list
		of dictionaries. By default, this list sorted by distance in ascending order. 
		clf (pkl): A KNN classifier used to predict the emotion of a color 


	Upon instantiation, each EmotaPal stores a WordPal and ColorPal object as properties. 
	"""
	
	def __init__(self, topn=100, unique_words = False, info=None ):
		self.topn = topn  
		self.unique_words  = unique_words
		self._info = info 
		self.clf =  joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "clf.pkl")) 
	
	@property
	def words(self):
		"""Instantiate a WordPal object based on EmotaPal's words"""
		return WordPal([x['emotion'] for x in self._info], self.unique_words)
	
	@property
	def colors(self):
		"""Instantiate a ColorPal object based on EmotaPal's colors"""
		return  ColorPal([x['color'] for x in self._info])

	@property 
	def info(self):
		"""Returns the information of the palette"""
		return self._info 

	
	def from_gimg(self, query, nimages):
		"""
		Returns an EmotaPal from a gimg search. 

		To return an EmotaPal, this function first finds the url
		top nimages for a query. This method then returns
		the dominant color of each image. The resulting color set 
		is treated as a color palette, and is fed into the from_colors
		constructor method. 

		Args:
			query (str): keywords to search google images for 
			nimages (int): number of images to attempt to fetch  

		Returns:
			EmotaPal object 
		"""
		urls = helpers.get_gimg_urls(query, nimages)
		imgs = [helpers.read_web_image(u) for u in urls]
		clrs = [ColorThief(i).get_color(quality=1) for i in imgs if i != "Failed"]
		assert (len(clrs) > 0), "Could not parse any urls :("
		return self.from_colors(clrs)

	def from_url(self, url, ncolors):
		"""Constructs an EmotaPal from a url."""
		img = helpers.read_web_image(url)
		if img != "Failed":
			return self.from_image(img, ncolors)
	
	def from_image(self, img, ncolors):
		"""Constructs an EmotaPal from an image"""
		colorthief = ColorThief(img)
		if ncolors == 1:
			clr =  colorthief.get_color(quality=1)
			return self.from_colors([clr])   
		elif ncolors > 1:
			clrs =  colorthief.get_palette(color_count=ncolors, quality=1)
			return self.from_colors(clrs)  
	
	def from_colors(self, clrs):
		"""Constructs an EmotaPal from a set of colors."""
		try:
			matches = [self.nearest_emotion(c) for c in clrs]
			self._info = self.parse_matches(matches)
			return self 
		except ValueError:
			raise ValueError("Could not parse colors. Please enter a list of colors.")


	def nearest_emotion(self, clr):
		"""
		Returns information on the nearest emotion to a color. 

		To find the "nearest emotion", we predict the emotion of 
		a color with a KNN classifier trained on a dataset with features 
		["Emotion", "Dominant Color"].  

		Args:
			self: self  
			color (list, tupple, or hex): an input color 

		Returns:
			dict: {
					"emotion": nearest emotion to an input color, 
					"distance": distance from input color to emotion color, 
					"color": input color
		}
		
		"""
		color = helpers.parse_color(clr)
		emotion = self.clf.predict([color])[0]
		distance = self.clf.kneighbors([color])[0][0][0]
		results =  {"emotion":emotion, "distance":distance, "color":color}
		return results

	def parse_matches(self, data):
		""" Returns the topn matches by shortest distance to input color. """
		top_matches = sorted(data, key=lambda x: x['distance'])[:self.topn]
		return top_matches

class WordPal():

	"""
	A WordPal is a list of words associated with a list of colors. 

	Attributes:
		_text (list): a list of words 

	"""

	def __init__(self, word_list=None, unique=False):
		self._text = word_list 
		self.unique =unique
	
	@property
	def sentiment(self):
		"""
		Returns the sentiment of a WordPal word list.

		Sentiment is computed by Affin, which ranks words
		on a neg/pos scale of [-5, 5]. 

		Returns:
			Sum of sentiment scores for each word in self.text 
		"""
		sentiment = Afinn().score(" ".join(self._text))
		return sentiment
	
	@property 
	def text(self):
		"""
		Returns the text of a word palette

		
		"""
		if self.unique:
			return list(OrderedDict.fromkeys(self._text))
		else:
			return self._text

class ColorPal():
	
	"""
	A ColorPal is a list of colors that is associated with a list of words. 

	Each ColorPal contains information about its colors, as well as a method
	for displaying itself as a color palette. 

	Attributes:
		colors (list): a list of colors 
	"""
	
	def __init__(self, color_list=None):
		self._colors = color_list
	
	@property
	def as_rgb(self):
		"""Returns a list of colors, each color a list of RGB values."""
		return self._colors

	@property 
	def as_hex(self):
		"""Returns a list of colors, each color a HEX string."""
		return [helpers.rgb2hex(c) for c in self._colors]

	def display(self, save_img=False):
		"""
		Displays a color palette of ColorPal colors.  

		Note that colors are displayed in descending order of best match. 
		So the first color is the color with the shortest distance to an emotion, etc. 
		"""

		clrs = self.as_hex
		sns.set(context="poster") # Make big 
		sns.palplot(clrs) # Create color palette 
		labels = helpers.label_palette(clrs, plt.gca(), save_img) 
		plt.show()
		plt.close()


