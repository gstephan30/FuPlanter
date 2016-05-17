#!/usr/bin/python
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
from datetime import datetime
import requests

sensor1 = Adafruit_DHT.DHT22
pin = 18
humidity, temperature = Adafruit_DHT.read_retry(sensor1, pin)
DewPoint = ((humidity / 100) ** 0.125) * (112 + 0.9 * temperature) + (0.1 * temperature) - 112
DewPointF = (((9.0 / 5.0) * DewPoint) + 32.0)
temperaturef = (((9.0 / 5.0) * temperature) + 32.0)

sensor2 = BMP085.BMP085()
pressureINC = (sensor2.read_pressure() * 0.000296133971008484)

data = {
    'ID': 'HERE_ID',
    'PASSWORD': 'HERE_PW3',
    'dateutc': str(datetime.utcnow()),
    'tempf': str(temperaturef),
    'humidity': str(humidity),
    'dewptf': str(DewPointF),
    'baromin': str(pressureINC),
    'action': 'updateraw',
    'softwaretype': 'RaspberryPi',
    'realtime': '1',
    'rtfreq': '2.5'
}
url = 'http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php'

r = requests.post(url=url, data=data)

#Raise exception if status code is not 200
r.raise_for_status()
print(r.text)

if humidity is not None and temperature is not None:
	print str(datetime.utcnow()) + '  TempDHT = {0:0.2f}*C  Humidity = {1:0.2f}%  '.format(temperature, humidity) + 'TempDHT = {0:0.2f}*F  '.format(temperaturef) + 'Dew Point = {0:0.2f}*C  '.format(DewPoint) + 'Dew Point = {0:0.2f} F  '.format(DewPointF) + 'TempBMP = {0:0.2f} *C  '.format(sensor2.read_temperature()) + 'Pressure = {0:0.2f} Pa  '.format(sensor2.read_pressure()) + 'Pressure = {0:0.2f} inch Mercury  '.format(pressureINC) + 'Altitude = {0:0.2f} m  '.format(sensor2.read_altitude()) + 'Sealevel Pressure = {0:0.2f} Pa  '.format(sensor2.read_sealevel_pressure())    
else:
	print 'Failed to get reading. Try again!'
