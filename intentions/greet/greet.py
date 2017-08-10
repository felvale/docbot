'''
Module designed to greet the user when greeted
'''

from app.db import makedb

def run_intent(req):
    '''
    The actual intent defined in this function. It will be called \
    when the system detecs this intent if configured correctly on \
    the intentions table
    '''
    req['answer'] = 'Hi!'

def prepare_db(conn):
    '''
    Create all the necessary DB tables and data for this module
    '''
    makedb.add_intention('greet', 'intention designed to greet back the user', \
                            'intentions.greet.greet', ['Hello, how are you doing?', \
                            'Hey, everything ok?', \
                            'Hi', 'Hello', 'hey'], conn)
