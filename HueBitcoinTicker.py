import json
import time
import requests
import xml.etree.ElementTree as ET

#global variables
previousPrice = 0

def loadConfigurationFile():
	return ET.parse('config.xml').getroot()

def setLightState(id, hue, bri, sat):
	payload = {"on": True, "hue": hue, "bri": bri, "sat": sat}
	response = requests.put(hubUrl + "/api/" + hubUsername + "/lights/" + str(lightId) + "/state", json=payload)

#load configuration data
config = loadConfigurationFile()
lightId = int(config.find('./light_id').text)
hubUrl = config.find('./hub_url').text
hubUsername = config.find('./hub_username').text
gdaxUrl = config.find('./gdax_url').text
intervalTimeSeconds = float(config.find('./interval_time_seconds').text)

while True:
	try:	
		#request bitcoin price
		response = requests.get(gdaxUrl)

		#success
		if response.status_code == 200:
			data = response.json()
			currentPrice = data["price"]

			if previousPrice > currentPrice:
				#red
				setLightState(1, 65535, 254, 254)
			elif previousPrice < currentPrice:
				#green
				setLightState(1, 25500, 254, 254)

			previousPrice = currentPrice
		#failure
		else:
			raise Exception('Something bad happened.')
	except:
		#yellow
		setLightState(1, 12750, 254, 254)

	#sleep
	time.sleep(intervalTimeSeconds)