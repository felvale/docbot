'''
Class regarding conections and other DB utilities
'''
from threading import Lock
from collections import deque
from app.config.configmanager import ConfigManager
import psycopg2

class MaxConnectionException(Exception):
    '''
    Exception raised when the max number of DB connections is reached
    '''

class DBUtils():
    '''
    Singleton that controls connection pools and session
    '''
    _util = None

    def __init__(self):
        self._connections = deque([])
        self._cur_connections = 0
        self._connection_lock = Lock()
        self._conection_string = 'host={0} user={1} dbname={1} password={2}'
        host = ConfigManager.get_manager().\
                        get_param('DBDATA', 'host')
        user = ConfigManager.get_manager().\
                        get_param('DBDATA', 'user')
        password = ConfigManager.get_manager().\
                        get_param('DBDATA', 'password')
        self._conection_string = self._conection_string.format(host, user, password)


    @staticmethod
    def get_instance():
        '''
        Get current instance of DBUtils
        '''
        if DBUtils._util is None:
            DBUtils._util = DBUtils()
            return DBUtils._util

        return DBUtils._util

    def get_connection(self):
        '''
        Get DB connection from connection pool
        '''

        self._connection_lock.acquire()
        if self._connections:
            conn = self._connections.popleft()
        else:
            if self._cur_connections < int(ConfigManager.get_manager().\
                                        get_param('DBDATA', 'maxconnections')):
                conn = psycopg2.connect(self._conection_string)
                self._cur_connections += 1
            else:
                raise MaxConnectionException('DB connections pool has already reached it\'s limit')
        self._connection_lock.release()
        return conn

    def close_connection(self, conn):
        '''
        Returns connection to connection pool, rolling back the transaction
        '''
        conn.rollback()
        self._connections.append(conn)
