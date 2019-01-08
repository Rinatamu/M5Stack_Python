from m5stack import *
import machine
import bme280
import time
import ujson
import urequests
import sys


lcd.setCursor(0, 0)
lcd.setColor(lcd.WHITE)
lcd.font(lcd.FONT_DejaVu24)
lcd.clear()


i2c = machine.I2C(scl=machine.Pin(2), sda=machine.Pin(5),freq=10000)
rtc = machine.RTC()
sys.tz ('UTC')
rtc.ntp_sync('ntp.nict.jp', update_period=3600)
for i in range(100):
    if rtc.synced():
        print('ntp synced.')
        lcd.print('ntp synced.',10,10)
        break
    print(i, end=' ')
    time.sleep_ms(10)

class sensordata:
    def __init__(self):
        self.posturl = 'https://api.powerbi.com/beta/37dfff33-d988-46f6-b952-590aba2b92e6/datasets/4bbecf96-35a1-4d4c-a835-15c71434b7e4/rows?key=2TdxEbYhaPu96BsPHTea%2Fzr2wKsOYxQVfGW0zs8hdM4%2BdJkf8BQF37vz1uO1z5B8ycJQ%2Fq%2BtHnHrJmzbo3vXsg%3D%3D'

    def timeset(self):
        timedata = rtc.now()
        prm_year = '{:0=4}'.format(timedata[0])
        prm_month = '{:0=2}'.format(timedata[1])
        prm_day = '{:0=2}'.format(timedata[2])
        prm_hour = '{:0=2}'.format(timedata[3])
        prm_minute = '{:0=2}'.format(timedata[4])
        prm_second = '{:0=2}'.format(timedata[5])

        self.datetime =  prm_year + "-" \
                +   prm_month + "-" \
                +   prm_day + "T" \
                +   prm_hour + ":" \
                +   prm_minute + ":" \
                +   prm_second + "Z"

    def bme280(self):
        bme280sensor = bme280.BME280(i2c=i2c)
        sendordata = bme280sensor.values
        self.temp  = sendordata[0]
        self.humi  = sendordata[2]
        self.pres  = sendordata[1]

    def display(self):
        lcd.clear()
        lcd.print(self.temp,10,10)
        lcd.print(self.humi,10,30)
        lcd.print(self.pres,10,50)
        lcd.print(self.datetime,10,90)

    def postpowerbi(self):
        pbheaders = {
            'Content-Type' :'application/json'
        }
        body = [
                {
                    "datetime" : self.datetime,
                    "temp" : float(self.temp),
                    "humi" : float(self.humi),
                    "pres" : float(self.pres)
                }
            ]
        body_json = ujson.dumps(body).encode("utf-8")
        res = urequests.post(
            self.posturl,
            data=body_json,
            headers=pbheaders
        )
        res.close()
        del res
        del body
        del body_json
        del pbheaders

sensor = sensordata()

while True:
    sensor.timeset()
    sensor.bme280()
    sensor.display()
    sensor.postpowerbi()
    time.sleep_ms(4000)
