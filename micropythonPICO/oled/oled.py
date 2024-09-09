from machine import Pin, SoftI2C
from oled.ssd1306 import SSD1306_I2C
from oled.logo import Logo
from time import sleep


class Oled(SSD1306_I2C):
    def __init__(self, scl_pin:int, sda_pin:int, width:int=128, height:int=64):
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.width = width
        self.height = height
        super().__init__(self.width, self.height, self.i2c)
        self.logos = Logo()
        self.logo_wifi = True
        
    
    def display_logo(self, name_logo:str, x:int=0, y:int=0):
        ''' display 'logo' at position (x,y)) '''
        fbuf = self.logos.get_logo(name_logo)
        self.blit(fbuf, x, y)
        
    def screen_wifi_connection(self):
        self.display_logo('papsdroid',0,0)
        self.display_logo('wifi64',64,0)
        self.display_logo('pi',48,28)
        self.rect(0,0,128,64,1)
        self.show()

    def blink_wifi(self):
        if self.logo_wifi:
            self.screen_wifi_connection()
        else:
            self.rect(64,0,127,63,0,True)
        self.rect(0,0,128,64,1)
        self.show()
        self.logo_wifi = not self.logo_wifi
    
    def screen_wifi_ok(self, ip_adress:str):
        self.fill(0)
        self.display_logo('wifi32',4,2)
        self.text('http://',40,40)
        self.text(ip_adress,8,50)
        self.rect(0,0,128,64,1)
        self.show()
    
    def screen_engine_off(self):
        self.display_logo('engine_off',84,2)
        self.show()

    def screen_engine_on(self):
        self.display_logo('engine_on',84,2)
        self.show()

    def screen_earth(self):
        self.display_logo('earth',45,2)
        self.show()
        
if __name__ == "__main__":
    oled = Oled(scl_pin=1, sda_pin=0)
    oled.display_logo('papsdroid',0,0)
    oled.display_logo('wifi64',64,0)
    oled.display_logo('pi',48,28)
    oled.rect(0,0,128,64,1)
    oled.show()