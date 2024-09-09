import time
from web.wifi import Wifi
from web.server import Event, Server
from web.config import OLED, MOTOR, DAYS

class EventPlanetarium(Event):
    """ This class manages event raised by the webserver to run planetarium"""
    def __init__(self)-> None:
        #Events managed by the web server
        super().__init__()
        
        #my own events
        self.EVENT_RUN1D: str = 'Tourne 1 jour'    #run planetarium for 1 day
        self.EVENT_RUN1W: str = 'Tourne 1 semaine' #run planetarium for 1 week
        self.EVENT_RUN1M: str = 'Tourne 1 mois'    #run planetarium for 1 month
        self.EVENT_RUN:   str = 'En marche'        #run planetarium
        self.EVENT_STOP:  str = 'STOP'             #stop planetarium
        
        #dictionnary of actions for each event name
        self.actions={
            self.EVENT_NONE: self.action_none,
            self.EVENT_RUN1D: self.action_run_1d,
            self.EVENT_RUN1W: self.action_run_1w,
            self.EVENT_RUN1M: self.action_run_1m,
            self.EVENT_RUN: self.action_run,
            self.EVENT_STOP: self.action_stop,
        }

    def action_run_1d(self):
        OLED.screen_engine_on()
        MOTOR.next_steps(DAYS['1D'])
        OLED.screen_engine_off()
    
    def action_run_1w(self):
        OLED.screen_engine_on()
        MOTOR.next_steps(DAYS['1W'])
        MOTOR.sleep()
        OLED.screen_engine_off()

    def action_run_1m(self):
        OLED.screen_engine_on()
        MOTOR.next_steps(DAYS['1M'])
        MOTOR.sleep()
        OLED.screen_engine_off()

    def action_run(self):
        OLED.screen_engine_on()
        while self.event_raised != self.EVENT_STOP:
            MOTOR.next_steps(DAYS['1D'])
        MOTOR.sleep()
        OLED.screen_engine_off()

    def action_stop(self):
        MOTOR.sleep()
        OLED.screen_engine_off()
    

class ServerWeb(Server):
    
    def __init__(self, debug:bool = False)-> None:
        MOTOR.sleep()
        super().__init__(wifi=Wifi(), event = EventPlanetarium(), debug=debug)
        
     
    def _gen_html(self)-> str:
 
        html = f"""<html>
            {self.HEAD_HTML}
            <body>
                <h1>Soleil-Terre-Lune</h1>
                <p><a href=https://papsdroidfr.github.io/tutoriels/soleil-terre-lune/> <Construire la maquette> </a></p>
                <p>Action en cours: <strong> {self.event_raised} </strong></p>
                <p><a href="/?event=runFull"><button class="button">Marche</button></a></p>
                <p><a href="/?event=run1D"><button class="button">1 jour</button></a></p>
                <p><a href="/?event=run1W"><button class="button">1 semaine</button></a></p>
                <p><a href="/?event=run1M"><button class="button">1 mois</button></a></p>
                <p><a href="/?event=stop"><button class="button button_red">STOP</button></a></p>
            </body>
        </html>"""
        
        return str(html)

    def _raise_event(self, request:str)-> None:
        """ Set event raised, depends on request"""
        if request.find('GET /?event=runFull') > -1:
            self.event.set_event(self.event.EVENT_RUN)
        elif request.find('GET /?event=stop') > -1:
            self.event.set_event(self.event.EVENT_STOP)
        
        elif self.event_raised != self.event.EVENT_RUN:
            if request.find('GET /?event=run1D') > -1:
                self.event.set_event(self.event.EVENT_RUN1D)
            elif request.find('GET /?event=run1W') > -1:
                self.event.set_event(self.event.EVENT_RUN1W)
            elif request.find('GET /?event=run1M') > -1:
                self.event.set_event(self.event.EVENT_RUN1M)
            else:
                self.event.set_event(self.event.EVENT_NONE)
        
        time.sleep(0.2)
    
            
#start web serveur
my_server = ServerWeb(debug=False)



