'''
Module designed to prepare DB base structure
'''
import getpass
import traceback
from app.config.configmanager import ConfigManager
from importlib import import_module
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def makedb():
    '''
    Generate base DB
    '''
    print('Starting to build db')
    host = input('Inform the hostname for the database: ')
    user = input('Inform the DB admin user: ')
    password = getpass.getpass('Inform the DB user password:')

    conn = psycopg2.connect('host=' + host + ' dbname=postgres user=' \
                                         + user + ' password=' + password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    bot_user = input('Determine the app DB username: ')
    if not search_role(conn, bot_user):
        create_role(conn, bot_user)

    if not search_db(conn):
        create_db(conn)

    conn.close()
    conn = psycopg2.connect('host=' + host + ' dbname=docbot user=' \
                                         + user + ' password=' + password)
    if not search_schema(conn):
        create_schema(conn)

    create_tables(conn)
    conn.commit()
    make_extensions(conn)
    conn.close()

def search_db(conn):
    '''
    Searches de database to verify if the application database was already created
    '''
    cur = conn.cursor()
    cur.execute('select datname from pg_database')
    res = cur.fetchall()
    for row in res:
        if row[0] == 'docbot':
            print('App base already created')
            cur.close()
            return True

    cur.close()

def create_db(conn):
    '''
    Creates an database for the application to use
    '''
    cur = conn.cursor()
    print('Couldn\' find the app base on DB, creating docbot database')
    cur.execute('CREATE DATABASE docbot WITH OWNER docbot')
    print('DB created')
    cur.close()

def search_role(conn, botuser):
    '''
    Checks if the application user was already created
    '''
    cur = conn.cursor()
    cur.execute('select rolname from pg_roles')
    res = cur.fetchall()
    for row in res:
        if row[0] == botuser:
            print('App user already created')
            cur.close()
            return True
    cur.close()

def create_role(conn, botuser):
    '''
    Creates the application user
    '''
    cur = conn.cursor
    print('Couldn\' find the app user on DB, creating' + botuser + ' user')
    app_password = getpass.getpass('Inform the APP user password: ')
    cur.execute('CREATE ROLE %s WITH ENCRYPTED PASSWORD %s', (botuser, app_password,))
    print('App user created')
    cur.close()

def search_schema(conn):
    '''
    checks if the table schema was already created
    '''
    cur = conn.cursor()
    cur.execute('select nspname from pg_namespace')
    res = cur.fetchall()
    for row in res:
        if row[0] == 'docbot':
            print('App schema already created')
            cur.close()
            return  True
    cur.close()

def create_schema(conn):
    '''
    Creates applicatinos tables schema
    '''
    cur = conn.cursor()
    print('Couldn\' find the app schema on DB, creating docbot schema')
    cur.execute('CREATE SCHEMA AUTHORIZATION docbot')
    print('Schema created')
    cur.close()

def create_tables(conn):
    '''
    Creates the base tables for bot functionality
    '''
    print('Generating tables if they don\'t exist')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS docbot.intentions( '    \
                    +'intention_id serial PRIMARY KEY,'             \
                    +'intention_name varchar(100),'                 \
                    +'intention_description varchar(300),'          \
                    +'intention_module varchar(300))')
    cur.execute('CREATE TABLE IF NOT EXISTS docbot.intentions_rel(' \
                'intention_tsvector tsvector,'                      \
                'intention_id bigint REFERENCES '                   \
                'docbot.intentions (intention_id))')
    cur.close()
    print('Base tables created')

def make_extensions(conn):
    '''
    Call installed modules make_db
    '''
    modules = ConfigManager.get_manager().get_param('INSTALLEDMODULES','installedmodules',True)
    for module in modules:
        try:
            mod = import_module(module)
            mod.prepare_db(conn)
        except Exception:
            print(traceback.format_exc())
