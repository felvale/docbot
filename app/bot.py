'''
Main bot control module, start, runs and clean bot resources
'''

from app.db.dbutils import DBUtils

class MainBot():
    '''
    Bot object class
    '''
    def __init__(self):
        self._input_thread = None
        self._interpret_threads = []

    def start_bot(self):
        '''
        Starts necessary resources for bot execution
        '''
        pass

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
