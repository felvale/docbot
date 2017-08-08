'''
Module defining the interpretes class resposinble for \
definning user intention
'''

import time
from app.threads.stopablethread import StopableThread
from app.config.configmanager import ConfigManager

class Interpreter(StopableThread):
    '''
    Interpreter thread class
    '''
    def __init__(self):
        StopableThread.__init__(self)

    def run(self):
        while True:

            time.sleep(ConfigManager.get_instance.get_param('IO', 'requestfrequency'))
            if self.check_run():
                break

        self.do_cleanup()

    def do_cleanup(self):
        '''
        Cleans necessary resources
        '''
        pass
