'''
Module defining the interpreter class responsible for \
definning user intention
'''

from importlib import import_module
from app.bot.distributor import Distributor
from app.threads.stopablethread import StopableThread
from app.config.configmanager import ConfigManager
from app.bot.dao import interpreterdao

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
        intent = None
        #attempt to find an intention that fits all input text
        found, int_name, int_module = interpreterdao.get_intention(req['message'], True)
        if not found:
            #attempt to find an intention that better fits the input
            found, int_name, int_module = interpreterdao.get_intention(req['message'], False)

        if found:
            print('Went with ' + int_name)
            try:
                intent = import_module(int_module)
            except ImportError:
                print('Could not load intention module')

        if intent is not None:
            intent.run_intent(req)
        else:
            req['answer'] = 'I don\'t know what you mean'
        self._output_module.do_output(req)
