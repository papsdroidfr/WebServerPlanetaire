''' manage the  PICO LEd
    
    args: none
    
    properties:
    - is_on: True/False
    
    methods
    - off(): switch off the led
    - on(): switch on the led 
    - blink(): switch on/off the led to make it blinked
'''

from machine import Pin
import time

class Led:
    def __init__(self)-> None:
        """ constructor """
        self._led = Pin("LED", Pin.OUT) #specific to PICO W
        self.off() #switch off the led.
        
    @property
    def is_on(self)-> bool:
        return(self._on)

    def off(self)-> None:
        """ Switch off the led. """
        self._led.value(0)
        self._on = False
        
    def on(self)-> None:
        """Switch on led."""
        self._led.value(1)
        self._on = True
        
    def blink(self) -> None:
        """Switch on/off led to make it blinked."""
        if self.is_on:
            self.off()
        else:
            self.on()

if  __name__ == '__main__':
    print('test module led.py')
    pico_led = Led()
    pico_led.on()
    time.sleep(3)
    pico_led.blink()
    print('bye')
    
    

