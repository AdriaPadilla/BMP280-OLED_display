# Librerias Sensor temp/hpa
from bmp280 import BMP280

# Librerias generales 
import time
from datetime import datetime
import json


############################
#       GET Raspby IP      #
############################

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

#############################


try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# Inicializando el modulo temperatura
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


#############################
#                           #
#   Modul pantalla OLED     # 
#                           #
#############################

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import socket

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()

image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)

disp.image(image)
disp.show()

# LIMPIEZA DE LA PANTALLA

disp.fill(0) 
disp.show()
image = Image.new('1', (128,64))
draw = ImageDraw.Draw(image)

#####################
# FUNCION PRINCIPAL #
#####################

def get_temp():
    # abrimos el archivo json
    with open("medidas.json", "r") as file:
        data = json.load(file)

    # Fecha de la toma
    get_time = datetime.now()
    now = get_time.strftime("%H:%M:%S %d-%m-%Y")
    dia = get_time.strftime("%d-%m-%y")
    hora = get_time.strftime("%H:%M:%S")
    try:
        temperatura = round(bmp280.get_temperature(),2)
        presion = round(bmp280.get_pressure(),3)
        # humedad = round(bme280.get_humidity(),3)
        print(f"Temp: {temperatura} //  Presion:{presion}hpa // El {now}")
        lectura = {}
        lectura["fecha"] = now
        lectura["temperatura"] = temperatura
        lectura["presion"] = presion
        data.append(lectura)

        draw.text((1,1), f'data: {dia}', fill=255)
        draw.text((1,10), f'hora: {hora}', fill= 255)
        draw.text((1,20), f'Temp: {temperatura}', fill=255)
        draw.text((1,30), f'Pres: {presion}', fill=255)
        draw.text((1,40), f'IP: {ip}', fill=255)
        disp.image(image)
        disp.show()
 
    except RuntimeError:
        lectura = {}
        lectura["fecha"] = now
        lectura["error"] = "RuntimeError: Unable to find bmp280 on 0x76, IOError"
        data.append(lectura)
        print("RuntimeError: Unable to find bmp280 on 0x76, IOError")


    with open("medidas.json", "w") as file:
        json.dump(data, file, indent=4)

get_temp()
    
