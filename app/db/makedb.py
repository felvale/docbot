'''

'''
import psycopg2

def makedb():
    print('Starting to build db')
    host = input('Inform the hostname for the database')

    conn = psycopg2.connect()
    cur = conn.cursor
    pass