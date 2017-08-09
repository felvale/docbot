'''
Main bot control module, start, runs and clean bot resources
'''

import time
from importlib import import_module
from app.config.configmanager import ConfigManager
from app.bot.interpreter import Interpreter
from app.db.dbutils import DBUtils

class MainBot():
    '''
    Bot object class
    '''
    def __init__(self):
        self._input_thread = None
        self._interpret_threads = []
        self._is_interactive = int(ConfigManager.get_instance().\
                                get_param('IO', 'interactiveprompt'))

    def start_bot(self):
        '''
        Starts necessary resources for bot execution
        '''
        input_mod = ConfigManager.get_instance().get_param('IO', 'inputmodule')
        self._input_thread = import_module(input_mod).InputThread()
        self._input_thread.start()
        interp_worker_count = int(ConfigManager.get_instance() \
                        .get_param('IO', 'interpreterworkercount'))
        for index in range(0, interp_worker_count):
            interpeter_worker = Interpreter(str(index + 1))
            interpeter_worker.start()
            self._interpret_threads.append(interpeter_worker)
            print('Started interpreter worker number: ' + str(index + 1))

        self.interactive_prompt()

    def clean_bot(self):
        '''
        Cleans all bot resources on close
        '''
        if self._input_thread is not None:
            self._input_thread.terminate()
            self._input_thread.join()

        for interp in self._interpret_threads:
            interp.terminate()
            interp.join()

        DBUtils.get_instance().clean_connections()

    def interactive_prompt(self):
        '''
        Controls the bots interactive prompt
        '''
        try:
            while True:
                if self._is_interactive:
                    command = input()
                    if command == 'stop':
                        break
                time.sleep(100)

        except KeyboardInterrupt:
            print('Stop requested with Ctrl + c')
        finally:
            print('Stoping bot')
            self.clean_bot()
