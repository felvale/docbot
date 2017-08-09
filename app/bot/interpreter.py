'''
Module defining the interpreter class responsible for \
definning user intention
'''

from importlib import import_module
from app.bot.distributor import Distributor
from app.threads.stopablethread import StopableThread
from app.config.configmanager import ConfigManager

class Interpreter(StopableThread):
    '''
    Interpreter thread class
    '''
    def __init__(self, number):
        StopableThread.__init__(self)
        self._refresh_time = float(ConfigManager.get_instance().get_param('IO', 'requestfrequency'))
        self._thread_reference = number
        out_module = ConfigManager.get_instance().get_param('IO', 'outputmodule')
        self._output_module = import_module(out_module)

    def run(self):
        distributor = Distributor.get_instance()
        has_req = distributor.get_received_event()
        while True:
            req = None
            has_req.wait(10)
            if distributor.has_next():
                req = distributor.get_next()
            if req:
                self.interp(req)

            if self.check_run():
                break
        self.do_cleanup()

    def do_cleanup(self):
        '''
        Cleans necessary resources
        '''
        pass

    def interp(self, req):
        '''
        Do interpretation
        '''
        temp_answer = 'Interpreting req on thread ' + self._thread_reference +  \
        '\nUser: ' + req['user'] +                                                \
        '\nUserId: ' + req['userid'] +                                            \
        '\nChannel: ' + req['channel'] +                                          \
        '\nMessage: ' + req['message'] +                                          \
        '\nHasLast: False'

        req['answer'] = temp_answer
        self._output_module.do_output(req)
