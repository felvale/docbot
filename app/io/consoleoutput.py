'''
Send exit message to console for testing pourposes \
disregarding user and channel as those are not used here
'''

def do_output(req):
    '''
    Do actual output
    '''
    print(req['answer'])
