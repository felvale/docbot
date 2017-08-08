'''
Base class for stopable thread
'''
import threading

class StopableThread(threading.Thread):
    '''
    Base class for all stopable threads
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self._terminate_event = threading.Event()

    def terminate(self):
        '''
        Signals the thread to terminate
        '''
        self._terminate_event.set()

    def check_run(self):
        '''
        Check if thread was signalled to stop
        '''
        return self._terminate_event.is_set()
