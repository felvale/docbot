'''
Singleton responsible for distributing inputs to \
Interpreters
'''
from collections import deque
from threading import RLock
from threading import Event

class Distributor():
    '''
    Distributor singleton that keeps request dicts
    '''
    dist_instance = None

    def __init__(self):
        self._pending_requests = deque([])
        self._request_list_lock = RLock()
        self._has_request_event = Event()

    @staticmethod
    def get_instance():
        '''
        Gets current instance of the distributor
        '''
        if Distributor.dist_instance:
            return Distributor.dist_instance

        Distributor.dist_instance = Distributor()
        return Distributor.dist_instance

    def add_request(self, request):
        '''
        Adds a request dict to be processed
        '''
        with self._request_list_lock:
            self._pending_requests.append(request)

        self._has_request_event.set()

    def has_next(self):
        '''
        Checks if there is a request to process
        '''
        with self._request_list_lock:
            return self._pending_requests

    def get_received_event(self):
        '''
        Returns the event handler for has request event
        '''
        return self._has_request_event

    def get_next(self):
        '''
        Get next request when there is one
        '''
        with self._request_list_lock:
            ret_req = self._pending_requests.popleft()
            if not self._pending_requests:
                self._has_request_event.clear()
            return ret_req
