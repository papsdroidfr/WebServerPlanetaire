''' config global variables of the web module:
    - WIFI-SSID: wifi ssid to connect
    - WIFI-PASSWORD: my wifi password
    - STATION: is the network.WLAN to activate
    - LED: led of PICO for managing connection status
        blinking: waiting for a wifi connection 
        green: web server started
        off: not wifi connexion.
'''

from web.led import Led
from oled.oled import Oled
from stepper.bipolar import BipolarStepper

#########################################
WIFI_SSID = "MY_WIFI_SSID"
WIFI_PASSWORD = "MY_WIFI_PASSWORD"
LED = Led()
OLED = Oled(scl_pin=1, sda_pin=0)
MOTOR = BipolarStepper(speed='high', direction='backward')
DAYS = {'1D': 200, '1W': 7*200, '1M': 30*200}
#########################################