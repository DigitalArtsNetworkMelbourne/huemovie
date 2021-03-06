from PIL import Image, ImageDraw
from beautifulhue.api import Bridge
from lib import TerminalSize, ColorHelper, Converter
from time import sleep
from sys import stdout
from colorama import Fore, Back, Style
import pyscreenshot as ImageGrab
import colorsys
import math
import os

sample_rate = 10							 # Frames per Second. Philips Hue documentation recommends no more than 10 requests per second, so try and stay below 10.
sample_size = 100							# Resize the screenshot to this size
brightness_threshold = 5					# Turn the lights off completely when brightness below this value (max 255)
density_threshold = 0.01					# Ignore colours below a certain density
num_globes = 3							  # Number of hue globes to update
ip = os.environ['HUE_BRIDGE_IP']			# IP of your Hue Bridge. nano ~/.bash_profile and add: export HUE_BRIDGE_IP="XXX.XXX.XXX.XXX"
username = os.environ['HUE_USERNAME']	   # Username set up on your Hue Bridge.
transition_time = 25

bridge = Bridge(device={ 'ip': ip }, user={ 'name': username })
converter = Converter()
terminalsize = TerminalSize()

def get_colours(image, resize, palettesize):
	image = image.resize((resize, resize))
	result = image.convert('P', palette=Image.ADAPTIVE, colors=palettesize)
	result.putalpha(0)
	colors = result.getcolors()

	return sorted(colors, reverse=True)

def colour_density(val,size):
	return val/math.pow(size,2)

def run():
	try:
		screenshot = ImageGrab.grab()
		colors = get_colours(screenshot, sample_size, num_globes)
		colors = [c for c in colors]
		colors += [None]*(num_globes-len(colors))
		x = 0
		resources = []

		for color in colors:
			x = x+1
			if color is None:
				resource = {
					'which': x,
					'data':{
						'state':{'on':False, 'transitiontime': transition_time}
					}
				}
			else:
				amt = color[0]
				r, g, b, a = color[1]
				density = colour_density(amt, sample_size)
				hsv = colorsys.rgb_to_hsv(r, g, b)
				xy = converter.rgbToCIE1931(r, g, b)
				hue,sat,bri = hsv
				state = bri>brightness_threshold and density>density_threshold

				resource = {
					'which': x,
					'data':{
						'state':{'on':state, 'xy':xy, 'bri': bri, 'transitiontime': transition_time}
					}
				}

			bridge.light.update(resource)
			resources.append((resource, r, g, b))
	except Exception as e:
		stdout.write("Exception: %s" % str(e))
		stdout.flush()


if __name__ == '__main__':
	while True:
		run()
		sleep((1000/sample_rate)/1000)
