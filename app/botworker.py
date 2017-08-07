'''
Module responsible for runing the bot loop
'''

import threading
from importlib import import_module
from app.config.configmanager import ConfigManager

class BotWorker(threading.Thread):
    '''
    Bot worker thread
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        inp_module = ConfigManager().get_instance().get_param('IO', 'inputmodule')
        self._input_module = import_module(inp_module)
        out_module = ConfigManager().get_instance().get_param('IO', 'outputmodule')
        self._output_module = import_module(out_module)

    def run(self):
        pass
