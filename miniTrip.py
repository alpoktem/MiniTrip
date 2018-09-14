from p5 import *
import sys
import os
from geopy.geocoders import Nominatim

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = WINDOW_WIDTH / 2
STOP_CIRCLE_WIDTH = 8

tripstop_geopoints = []   #(Longitude, Latitude) list
tripstop_names = []

def setup():
	size(WINDOW_WIDTH, WINDOW_HEIGHT)
	title('MiniTrip')
	populate_tripstop_geopoints()
	

def populate_tripstop_geopoints():
	geolocator = Nominatim(user_agent="MiniTrip")
	print("Loaded geolocator")
	print("Tripstops: ", tripstop_names)
	for stop in tripstop_names:
		try:
			location = geolocator.geocode(stop)
		except:
			location = None
			print("Geocoder fail")

		if location == None:
			print("Cannot figure out where %s is :("%stop)
		else:
			tripstop_geopoints.append(location.point)
	print("Populated stop coordinate list")
	print(tripstop_geopoints)

def draw():
	background(255)

	last_tripstop_windowpoint = None
	for tripstop_index, tripstop_geopoint in enumerate(tripstop_geopoints):
		curr_tripstop_windowpoint = geopoint_to_windowpoint(tripstop_geopoint, WINDOW_WIDTH, WINDOW_HEIGHT)
		if tripstop_index == 0:
			fill(0, 255, 0, 200)
		elif tripstop_index == len(tripstop_geopoints) - 1:
			fill(255, 0, 0, 200)
		else:
			fill(0, 0, 0, 255)
		circle(curr_tripstop_windowpoint, STOP_CIRCLE_WIDTH)
		if not last_tripstop_windowpoint == None:
			line(last_tripstop_windowpoint, curr_tripstop_windowpoint)
		last_tripstop_windowpoint = curr_tripstop_windowpoint
	print("Drew %i stops."%(tripstop_index+1))	
	no_loop()

def key_pressed(event):
	if event.key == 'Q' or event.key == 'q':
		sys.exit()
	if event.key == 'R' or event.key == 'r':
		loop()

def geopoint_to_windowpoint(geopoint, window_width, window_height):
	assert geopoint[1] <= 180 and geopoint[1] >= -180
	assert geopoint[0] <= 90 and geopoint[0] >= -90

	#windowpoint = (window_width/2 + (geopoint[1]/180) * (window_width/2), window_height/2 - (geopoint[0]/90) * (window_height/2))
	windowpoint = (50 + (geopoint[1]/180) * (window_width), window_height - (geopoint[0]/90) * (window_height))
	return windowpoint

if __name__ == '__main__':
	stops_file = sys.argv[1]
	print("Trip stops file: ", stops_file)

	with open(stops_file) as f:
		for stop in f:
			if not stop.startswith("#"):
				tripstop_names.append(stop.strip())
	run()