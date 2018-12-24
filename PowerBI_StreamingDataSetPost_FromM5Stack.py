from m5stack import *
import time
import ujson
import urequests
import machine

lcd.setCursor(0, 0)
lcd.setColor(lcd.WHITE)
lcd.font(lcd.FONT_DejaVu24)
lcd.clear()

class powerbi:
    def __init__(self):
        self.rtc = machine.RTC()
        self.rtc.ntp_sync('ntp.nict.jp', update_period=3600)
        
        # PowerBI ストリーミングデータセットのURLを入れる
        self.posturl = ''

    def timeset(self):
        timedata = self.rtc.now()
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
    
    def postpowerbi(self,btn):
        self.btn = btn

        pbheaders = {
            'Content-Type' :'application/json'
        }

    
        if "A" in self.btn:
            body = [
                {
                    "datetime" : self.datetime,
                    "A" : 1,
                    "B" : 0,
                    "C" : 0
                }
            ]
            body_json = ujson.dumps(body).encode("utf-8")

        elif "B" in self.btn:
            body = [
                {
                    "datetime" : self.datetime,
                    "A" : 0,
                    "B" : 1,
                    "C" : 0
                }
            ]
            body_json = ujson.dumps(body).encode("utf-8")

        elif "C" in self.btn:
            body = [
                {
                    "datetime" : self.datetime,
                    "A" : 0,
                    "B" : 0,
                    "C" : 1
                }
            ]
            body_json = ujson.dumps(body).encode("utf-8")

        else:
            test = "aaa"
        
        print(body_json)
        res = urequests.post(
            self.posturl,
            data=body_json,
            headers=pbheaders
        )
        res.close()


PowerBI = powerbi()

while True:
    PowerBI.timeset()
    if buttonA.wasPressed():
        PowerBI.postpowerbi("A")
    
    if buttonB.wasPressed():
        PowerBI.postpowerbi("B")
    
    if buttonC.wasPressed():
        PowerBI.postpowerbi("C")

    time.sleep(0.5)
