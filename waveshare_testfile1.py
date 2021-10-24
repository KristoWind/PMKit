from gsmHat import GSMHat, SMS, GPS
gsm = GSMHat('dev/ttyS0', 115200)

# GPS data logging
GPSObj=gsm.GetActualGPS()

print('GNSS_status: %s' % str(GPSObj.GNSS_status))
print('Fix_status: %s' % str(GPSObj.Fix_status))
print('UTC: %s' % str(GPSObj.UTC))
print('Latitude: %s' % str(GPSObj.Latitude))
print('Longitude: %s' % str(GPSObj.Longitude))
print('Altitude: %s' % str(GPSObj.Altitude))
print('Speed: %s' % str(GPSObj.Speed))
print('Course: %s' % str(GPSObj.Cpurse))
print('HDOP: %s' % str(GPSObj.HDOP))
print('PDOP: %s' % str(GPSObj.HDOP))
print('HDOP: %s' % str(GPSObj.PDOP))
print('VDOP: %s' % str(GPSObj.VDOP))
print('GPS_satellites: %s' % str(GPSObj.GPS_satellites))
print('GNSS_satellites: %s' % str(GPSObj.GNSS_satellites))
print('Signal: %s' % str(GPSObj.Signal))








