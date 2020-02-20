#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google_images_download import google_images_download  
import sys, io
from urllib.request import urlopen
from colorthief import ColorThief 
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from requests.exceptions import HTTPError
from urllib.error import HTTPError

"""Helper functions for the emotapal package"""

def parse_color(clr):
	"""Returns an RGB list if color is RGB, and converts a hex color to RGB otherwise"""
	if type(clr) == str:
		return hex2rgb(clr)
	elif type(clr) == list:
		return clr
	elif type(clr) == tuple:
		return list(clr)

def hex2rgb(color):
	"""Converts a hex str to RGB list"""
	rgb_clr = list(tuple(bytes.fromhex("{}".format(color.strip("#")))))
	return rgb_clr

def rgb2hex(color):
	"""Converts an RGB tupple or list to a hex string"""
	hex_clr = "#" + bytes(color).hex()
	return hex_clr

def read_web_image(url):
	"""Tries to read in an image via url"""
	result = "Failed"
	try:
		result = io.BytesIO(urlopen(url).read())
	except HTTPError as e:
		print(e)
	except ValueError as e:
		print("Bad url given")
	except Exception as e:
		print("Could not read image")
	return result 

def get_gimg_urls(search_term, n):
	"""Returns `n` Google Image urls for a given `search_term`"""
	f = write_gimg_urls(search_term, n)
	urls = parse_gimg_urls(f)
	return urls

def write_gimg_urls(search_term, n):
	"""Write `n` Google Image urls for a `search_term` to a text file"""
	f = open('URLS.txt', 'w') # Open text file to write print output to
	orig_stdout, sys.stdout = sys.stdout, f # Keep location of original sys.stdout  
	response = google_images_download.googleimagesdownload() # Get images
	arguments = {"keywords":search_term + " –no-download" , "limit":n, "print_urls":True} #Don't download, but print urls
	paths = response.download(arguments) 
	sys.stdout = orig_stdout # Switch to normal print output, close file
	f.close()
	return f

def parse_gimg_urls(urls):
	"""Parses output of Gogle Image results to return urls"""
	with open('URLS.txt') as f: content = f.readlines()
	urls = [content[j-1][11:-1] for j in range(len(content)) if content[j][:9] == 'Completed']
	return urls    

def gimg_color_reader(img):
	"""
	Catch ColorThief exceptions. 

	For the `from_img` and `from_url` constructors, let ColorThief 
	*throw* exceptions if an image won't load. But if there are many images, 
	it is not fatal if some don't load. 
	"""
	try: 
		return ColorThief(img).get_color(quality=1)
	except:
		pass

def label_palette(clrs, ax, save_img):
	"""Labels a custom color palette"""
	for i, name in enumerate(clrs):
		ax.text(i, 0.5, name, 
			fontsize= 8 * int(3.0/len(clrs)+1), 
			bbox= dict(facecolor='white', alpha=0.75), 
			ha="center", va="center"
		) 
	if save_img: 
		dt = datetime.now().strftime("%m.%d.%Y.%H:%M:%S")
		plt.tight_layout()
		plt.savefig("{}.png".format(dt), dpi=300, bbox_inches="tight")
	return ax
