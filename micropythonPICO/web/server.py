import time, socket, _thread
from web.config import LED
from web.log import log_info, log_warn, log_error
from web.wifi import Wifi


class Event():
    """ This class manages event raised by the webserver
        Each event (except event "none") is associated to an action_xxx() method
        TODO: build and override your own action methods
        
        Args: None
        
        Attributes:
            EVENT_xxx (srt): static event name
            event_raised (str): name of the event raised
    """
    
    def __init__(self)-> None:
        #Event names managed by the web server
        #TODO: put as many other different event names as you wish
        self.EVENT_NONE:str = 'none'
        self.EVENT_TEST:str = 'test'
        self.EVENT_STOP:str = 'stop'
        
        #dictionnary of actions for each event name
        self.actions={
            self.EVENT_NONE: self.action_none,
            self.EVENT_TEST: self.action_test,
            self.EVENT_STOP: self.action_stop,
        }
        
        self._event_raised = self.EVENT_NONE
        
        
    def set_event(self, event:str)-> None:
        """Setter _event_name."""
        self._event_raised = event
    
    @property
    def event_raised(self)-> str:
        """Getter _event_raised."""
        return self._event_raised
    
    def action_none(self)-> None:
        """do nothing"""
        pass
    
    def action_stop(self)-> None:
        """Action raised by event stop."""
        print('Action STOP.')
    
    def action_test(self)-> None:
        """Action raised by event test."""
        print('Start action TEST.')
        time.sleep(2)
        print('End action TEST.')


class Server():
    """ This class manage the web server.
        Start listing to events in a new thread,
        then start web service in the main thread.
        
        Args:
            wifi (Wifi): the wifi connection to use (default None)
            event (Event): events managed by the web server
            debug (bool, default False): if True logs are printed.
        
        Attributes:
            event_raised (str): event name raised by web server
    """
    
    def __init__(self, wifi:Wifi = None,
                 event: Event =  Event(),
                 debug:bool = False,
        )-> None:
        """ Constructor """
        self._wifi: Wifi = wifi       #wifi connection
        self.debug: bool = debug      #debug mode True/False
        self.event: Event = event     #event raised by the web server
        #static CSS style used by HTML page
        self.CSS_STYLE: str =  """
            <style> html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                h1{color: #3F1BF4; padding: 2vh;}
                p{font-size: 1.5rem;}
                .button{display: inline-block; background-color: #4286f4; border: blue solid 1px; 
                    border-radius: 4px; color: white; padding: 16px 40px;
                    text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
                .button_red{background-color: #b8061c;}
            </style>
        """
        #static <head></head> section used by HTML page
        self.HEAD_HTML: str = f"""
            <head>
                <title>PICO Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="icon" href="data:,">
                { self.CSS_STYLE }
            </head>
        """
        
        if self._wifi == None:
            log_error('Connect first to a WIFI.', self.debug)
        else:
            #start thread that react to event
            _thread.start_new_thread(self._thread_loop_event, ())
        
            #start WEB server
            try:
                self._start()
            except KeyboardInterrupt:
                if self.debug:
                    log_warn('KeyboardInterrupt, bye.')
            except OSError as err:
                if self.debug:
                    log_warn(f'something went wrong. {err}')
            finally:
                self._close()
                _thread.exit()
                log_error('Exiting...', self.debug)


    @property
    def _my_html_page(self)-> str:
        """Returns: the html code generated."""
        return self._gen_html()
    
    @property
    def event_raised(self)-> str:
        """Returns: event.event_raised."""
        return self.event.event_raised

    def _start(self)-> None:
        """Start the server, looping into request."""
        if self.debug:
            log_info('Starting web server...')
        try:
            self._s = socket.socket()
            self._s.bind((self._wifi.ip_adress, 80))
            self._s.listen(1)
        except OSError as err:
            if self.debug:
                log_warn(f'Something went wrong ...{err}')
            self._close()
            log_error('Exiting...', self.debug)
        LED.on()
        if self.debug:
            log_info(f'Web serveur started, listing for requests from http://{self._wifi.ip_adress}')
        self._loop_request() #infinite loop into requests received
        

    def _loop_request(self)-> None:
        """Infinite loop into requests received."""
        while True:
            conn, addr = self._s.accept()
            if self.debug:
                log_info('Got a connection from %s' % str(addr))
            request = str(conn.recv(1024))
            request_get = request[:request.find('HTTP')] #extract GET request
            if self.debug:
                log_info('Content: '+ request_get)
            self._raise_event(request_get)  # update event based on request received
            response = self._my_html_page    # build a dynamic new HTML page
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()

    def _close(self)-> None:
        """Close the server and release ressources."""
        LED.off()
        self._s.close() # mark the socket closed and release all ressource
        if self.debug:
            log_info('Web server is closed.')


    def _thread_loop_event(self)-> None:
        """Infinite loop of actions based on events raised by web server."""
        while True:
            self.event.actions[self.event_raised]()     #run action of the event
            self.event.set_event(self.event.EVENT_NONE) #set event none when action is complete
            time.sleep(0.2)
        
        
    def _gen_html(self) -> str:
        """ HTML code generator
            TODO: Override this method with your own
            Returns: the HTML code in str format     
        """
  
        html = f"""<html>
            {self.HEAD_HTML}
            <body>
                <h1>Hello PICO WWWorld!</h1> 
                <p>Event raised: <strong> {self.event_raised} </strong></p>
                <p><a href="/?event=test"><button class="button">TEST</button></a></p>
                <p><a href="/?event=stop"><button class="button button_red">STOP</button></a></p>
            </body>
        </html>"""
        
        return str(html)
    
    
    def _raise_event(self, request:str)-> None:
        """ Set event raised, depends on request
            TODO: Override this method with your own
            Args: request (str) is the request read on a socket
        """
        if request.find('GET /?event=test') > -1:
            self.event.set_event(self.event.EVENT_TEST)
        elif request.find('GET /?event=stop') > -1:
            self.event.set_event(self.event.EVENT_STOP)
        else:
            self.event.set_event(self.event.EVENT_NONE)
  


if  __name__ == '__main__':
    print('Test module server.py')
    try:
        my_nowifi_server=Server()
    except:
        pass
    my_server=Server(wifi=Wifi(), debug=True)
    
    
        
    
    
