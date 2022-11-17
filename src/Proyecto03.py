import board
import busio
import time
import adafruit_bmp280
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gpiozero import Buzzer
from gpiozero import MotionSensor

# defining the scope of the application
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 

#credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope) 

# authorize the clientsheet 
client = gspread.authorize(cred)

# get the sample of the Spreadsheet
sheet = client.open("Laboratorio7")

worksheet = sheet.worksheet("datos")
worksheetData = sheet.worksheet("DatosTransformar")

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)


buzzer_zumbador = Buzzer(24)# GPIO 24 o 18 en raspi
pir = MotionSensor(23) #GPIO 23 o 16 en la raspi
buzzer_zumbador.off()

sensor.sea_level_pressure=1013.25
coord = worksheet.cell (2, 5) .value
ID = int(coord)

while True:
    pir.wait_for_motion()
    buzzer_zumbador.on()
    print("Movimiento detectado")
    temp = round(sensor.temperature, 2)
    worksheet.update_cell(2+ID,1,str(temp))
    worksheetData.update_cell(ID+1,1,str(temp))
    press = round(sensor.pressure, 2)
    worksheet.update_cell(2+ID,2,str(press))
    alt = round(sensor.altitude, 2)
    worksheet.update_cell(2+ID,3,str(alt))
    print("Temperature: "+ str(temp) + "°C  "+"Pressure: "+str(press)+"   Altitude: " + str(alt))
    ID = ID + 1
    worksheet.update_cell(2,5,str(ID))
    pir.wait_for_no_motion()
    buzzer_zumbador.off()
    print("Movimiento no detectado")
    time.sleep(1)