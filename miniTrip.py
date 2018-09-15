from p5 import *
import sys
import os
from geopy.geocoders import Nominatim

STOP_CIRCLE_WIDTH = 7
SCALE = 40
CROP = True
MARGIN_RATIO = 0.1
SQUARED = True 

tripstop_geopoints = []   #(Longitude (0-360), Latitude(0-180)) list
tripstop_names = []

lat_min = 0
lat_max = 180
long_min = 0
long_max = 360
margin_x = 0
margin_y = 0
x_displacement = 0
y_displacement = 0

def setup():
	global lat_min, lat_max, long_min, long_max
	global margin_x, margin_y
	global x_displacement, y_displacement
	populate_tripstop_geopoints()
	if CROP:
		lat_min, lat_max, long_min, long_max = determine_edgepoints()
	window_width, window_height, margin_x, margin_y, x_displacement, y_displacement = determine_window_size(lat_min, lat_max, long_min, long_max, SCALE)
	print('window size, %i,%i'%(window_width, window_height))
	size(window_width, window_height)
	title('MiniTrip')

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
			tripstop_geopoints.append(to_geopoint(location.point))
	print("Populated stop coordinate list")
	print(tripstop_geopoints)

#converts a proper geolocation into geopoint
def to_geopoint(geolocation):
	return (geolocation[1] + 180, 90 - geolocation[0])

def determine_edgepoints(squared=SQUARED):
	assert len(tripstop_geopoints) > 0
	
	long_min = long_max = tripstop_geopoints[0][0]
	lat_min = lat_max = tripstop_geopoints[0][1]
	print('lat_min', lat_min)
	print('lat_max', lat_max)
	print('long_min', long_min)
	print('long_max', long_max)
	print("=====")

	for geopoint in tripstop_geopoints:
		print(geopoint)
		if geopoint[0] < long_min:
			long_min = geopoint[0]
			print('long_min', long_min)
		elif geopoint[0] > long_max:
			long_max = geopoint[0]
			print('long_max', long_max)
		if geopoint[1] < lat_min:
			lat_min = geopoint[1]
			print('lat_min', lat_min)
		elif geopoint[1] > lat_max:
			lat_max = geopoint[1]
			print('lat_max', lat_max)

	print("=====")
	print('lat_min', lat_min)
	print('lat_max', lat_max)
	print('long_min', long_min)
	print('long_max', long_max)

	return lat_min, lat_max, long_min, long_max

def determine_window_size(lat_min, lat_max, long_min, long_max, scale=SCALE, margin_ratio=MARGIN_RATIO, squared=SQUARED):
	height = scale*(lat_max - lat_min)
	width = scale*(long_max - long_min)

	margin_x = width*margin_ratio
	margin_y = height*margin_ratio

	x_displacement = 0
	y_displacement = 0

	if squared:
		if height > width:
			x_displacement = (height - width) / 2
			y_displacement = 0
			width = height
			margin_x = margin_y
			width = height = heigth + margin_y*2
		elif width > height:
			y_displacement = (width - height) / 2
			x_displacement = 0
			height = width
			margin_y = margin_x
			height = width = width + margin_x*2
	else:
		height = height + margin_y*2
		width = width + margin_x*2

	print('x_displacement', x_displacement)
	print('y_displacement', y_displacement)

	return width, height, margin_x, margin_y, x_displacement, y_displacement

def geopoint_to_windowpoint(geopoint, scale=SCALE):
	x = scale*(geopoint[0] - long_min) + margin_x + x_displacement
	y = scale*(geopoint[1] - lat_min) + margin_y + y_displacement

	print("windowpoint %f,%f"%(x,y))
	return (x,y)

def draw():
	background(255)
	print("DRAW")
	print('lat_min', lat_min)
	print('lat_max', lat_max)
	print('long_min', long_min)
	print('long_max', long_max)
	print('margin_x', margin_x)
	print('margin_y', margin_y)
	last_tripstop_windowpoint = None
	for tripstop_index, tripstop_geopoint in enumerate(tripstop_geopoints):
		print('geopoint, ', tripstop_geopoint)
		curr_tripstop_windowpoint = geopoint_to_windowpoint(tripstop_geopoint)
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

if __name__ == '__main__':
	stops_file = sys.argv[1]
	print("Trip stops file: ", stops_file)

	with open(stops_file) as f:
		for stop in f:
			if not stop.startswith("#"):
				tripstop_names.append(stop.strip())
	run()