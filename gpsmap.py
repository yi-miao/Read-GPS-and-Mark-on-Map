# 1. Raspberry Pi 4B
# 2. NEO-6M GPS Module
# 3. FTDI USB Serial Adapter Module
# 4. PiOS: Bullseye
# 5. Python packages/modules: serial, folium, webbrowser
# 6. Python script: gpsmap.py

from serial import Serial           
import folium
import webbrowser
from time import sleep

class Gpsmap:
	def __init__(self, port='COM5', rate=9600, mapfile='mmap.html'):
		self.port = port
		self.rate = rate
		self.ser = Serial(self.port, self.rate, timeout=1) 
		self.lat = 0.0
		self.lon = 0.0
		self.map = ''
		self.mapfile = mapfile

	def convert(self, value):
		deci = float(value)/100.00
		intg = round(deci)
		resi = (deci - intg)/0.6
		posi = intg + resi
		return posi

	def readGps(self):
		while True:
			try:
				line = self.ser.readline().decode('utf-8').rstrip()
				if line.startswith('$GPGGA'):
					fields = line.split(',')
					self.lat = self.convert(fields[2])
					self.lon = self.convert(fields[4])
					if [self.lat, self.lon] != [0.0, 0.0]:
						break
			except:
				sleep(0.5)
				pass

	def createMap(self):
		home = (self.lat, -self.lon)	# adjust for lognitude west
		citycenter = (43.59333741168578, -79.64241745396272)
		route = [
		    home,
		    citycenter,
		]
		self.map = folium.Map(location=home, zoom_start=14.2)
		folium.Marker(location=home, tooltip="home").add_to(self.map)
		folium.Marker(location=citycenter, tooltip="city center").add_to(self.map)
		folium.PolyLine(route, tooltip="route").add_to(self.map)
		self.map.save(self.mapfile)

	def showMap(self):
		webbrowser.open(self.mapfile, new=2)

if __name__ == '__main__':
	gp = Gpsmap()
	gp.readGps()
	gp.createMap()
	gp.showMap()