'''
Module defining the Console Thread class responsible for \
capturing user input in test environment
'''

import time
from app.bot.distributor import Distributor
from app.threads.stopablethread import StopableThread
from app.config.configmanager import ConfigManager

class InputThread(StopableThread):
    '''
    Console Input thread class
    '''
    def __init__(self):
        StopableThread.__init__(self)
        self._refresh_time = float(ConfigManager.get_instance().get_param('IO', 'requestfrequency'))

    def run(self):
        distributor = Distributor.get_instance()
        while True:
            message = input('')
            distributor.add_request(self.prepare_req(message))
            if self.check_run():
                break
            time.sleep(self._refresh_time)
        self.do_cleanup()

    def do_cleanup(self):
        '''
        Cleans necessary resources
        '''
        pass

    def prepare_req(self, message):
        '''
        Prepare req dict with the received message, searchind for historic message
        '''
        req = {'user': 'Console User', 'userid': 'N/A', 'channel':'N/A', 'message':message}
        return req
