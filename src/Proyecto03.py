# Universidad Del Valle de Guatemala
# Copyright (C), 2022-2023, bl33h, MelissaPerez09, FabianJuarez182, SebasJuarez
# @author Sara Echeverria, Melissa Perez, Fabian Juarez, Sebastian Juarez
# FileName: Proyecto03
# Descripcion del programa: programacion de sensores de entrada y salida

# Libraries
import board
import busio
import time
import adafruit_bmp280
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gpiozero import Buzzer
from gpiozero import MotionSensor

# Defines the scope of the application
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 

# Credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope) 

# Authorize the clientsheet 
client = gspread.authorize(cred)

# Get the sample of the Spreadsheet
sheet = client.open("Laboratorio7")

# Get the sample sheet of the Spreadsheet
worksheet = sheet.worksheet("datos")
worksheetData = sheet.worksheet("DatosTransformar")

# Configuration of temperature sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Assigns GPIO pin for Raspberry pi 
buzzer_zumbador = Buzzer(24)            # GPIO 24 o 18 en raspi
pir = MotionSensor(23)                  # GPIO 23 o 16 en la raspi
buzzer_zumbador.off()                   # Initialize buzzer in off

# Configuration of sensor
sensor.sea_level_pressure=1013.25       # Preassure level
coord = worksheet.cell (2, 5) .value    # Next position to save data
ID = int(coord)                         # Assigns ID to the position

# Cycle to execute the main function
while True:
    # Initializes motion sensor and buzzer
    pir.wait_for_motion()
    buzzer_zumbador.on()
    # Message for movement
    print("Movimiento detectado")

    # - Save data of temperature, pressure and altitude -
    # Temperature capture
    temp = round(sensor.temperature, 2)
    # .update: saves data in worksheet 1, column 1, row ID+1
    worksheet.update_cell(2+ID,1,str(temp))
    # .update: saves data in worksheet 2, column 1, row ID+1
    worksheetData.update_cell(ID+1,1,str(temp))
    # Pressure capture
    press = round(sensor.pressure, 2)
    # .update: saves data in worksheet 1, column 2, row ID+2
    worksheet.update_cell(2+ID,2,str(press))
    # Altitude capture
    alt = round(sensor.altitude, 2)
    # .update: saves data in worksheet 1, column 3, row ID+2
    worksheet.update_cell(2+ID,3,str(alt))

    # Message for all captured data
    print("Temperature: "+ str(temp) + "°C  "+"Pressure: "+str(press)+"   Altitude: " + str(alt))
    
    # Updates ID
    ID = ID + 1

    # Update information for next position: saves data in worksheet 1, column 5, row 2
    worksheet.update_cell(2,5,str(ID))
    # pir sensor no detecting movement
    pir.wait_for_no_motion()
    # Buzzer off
    buzzer_zumbador.off()
    # Message for no movement
    print("Movimiento no detectado")
    # Sleep
    time.sleep(1)