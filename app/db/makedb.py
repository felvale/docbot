'''
Module designed to prepare DB base structure
'''
import getpass
from importlib import import_module
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.config.configmanager import ConfigManager

def makedb():
    '''
    Generate base DB
    '''
    try:
        print('Starting to build db')
        host = input('Inform the hostname for the database: ')
        user = input('Inform the DB admin user: ')
        for index in range(0, 3):
            try:
                if index == 2:
                    print('Exceeded limit of tries')
                    return
                password = getpass.getpass('Inform the DB user password:')
                conn = psycopg2.connect('host=' + host + ' dbname=postgres user=' \
                                         + user + ' password=' + password)
                break
            except psycopg2.OperationalError:
                print('Incorrect password')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        bot_user = input('Determine the app DB username: ')
        if not search_role(conn, bot_user):
            create_role(conn, bot_user)

        if not search_db(conn, bot_user):
            create_db(conn, bot_user)

        conn.close()
        for index in range(0, 3):
            try:
                if index == 2:
                    print('Exceeded limit of tries')
                    return
                app_password = getpass.getpass('Inform the APP user password: ')
                conn = psycopg2.connect('host=' + host + ' dbname=docbot user=' \
                                         + bot_user + ' password=' + app_password)
                break
            except psycopg2.OperationalError:
                print('Incorrect password')
        if not search_schema(conn, bot_user):
            create_schema(conn, bot_user)

        create_tables(conn)
        conn.commit()
        make_extensions(conn)
        conn.close()
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as excep:
        print('Error connecting to DB and running commands, message follows')
        print(excep.message)

def search_db(conn, botuser):
    '''
    Searches de database to verify if the application database was already created
    '''
    cur = conn.cursor()
    cur.execute('select datname from pg_database')
    res = cur.fetchall()
    for row in res:
        if row[0] == botuser:
            print('App base already created')
            cur.close()
            return True

    cur.close()

def create_db(conn, botuser):
    '''
    Creates an database for the application to use
    '''
    cur = conn.cursor()
    print('Couldn\' find the app base on DB, creating ' + botuser + ' database')
    cur.execute('CREATE DATABASE ' + botuser + ' WITH OWNER ' + botuser)
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
    app_password = getpass.getpass('Inform the APP user password: ')
    cur = conn.cursor()
    print('Couldn\' find the app user on DB, creating' + botuser + ' user')
    cur.execute('CREATE ROLE ' + botuser + ' WITH ENCRYPTED PASSWORD %s', (app_password,))
    cur.execute('ALTER ROLE ' + botuser + ' WITH LOGIN')
    print('App user created')
    cur.close()

def search_schema(conn, botuser):
    '''
    checks if the table schema was already created
    '''
    cur = conn.cursor()
    cur.execute('select nspname from pg_namespace')
    res = cur.fetchall()
    for row in res:
        if row[0] == botuser:
            print('App schema already created')
            cur.close()
            return  True
    cur.close()

def create_schema(conn, botuser):
    '''
    Creates applicatinos tables schema
    '''
    cur = conn.cursor()
    print('Couldn\' find the app schema on DB, creating docbot schema')
    cur.execute('CREATE SCHEMA AUTHORIZATION ' + botuser)
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
    modules = ConfigManager.get_instance().get_param('INSTALLEDMODULES', 'installedmodules', True)
    for module in modules:
        print('Preparing DB for ' + module)
        try:
            mod = import_module(module)
            mod.prepare_db(conn)
        except AttributeError:
            print('Module ' + module + ' DoesN\'t have an prepare_db function')

def add_intention(name, desc, module, calllist, conn):
    '''
    Adds an intention to DB
    '''
    cur = conn.cursor()

    cur.execute('INSERT INTO intentions(intention_name, intention_description, intention_module)' \
                    + 'select %s, %s, %s where not exists (select 1 from intentions where '\
                    + 'intention_name = %s)'                                             \
                    , (name, desc, module, name))          \


    for call in calllist:
        cur.execute('INSERT INTO intentions_rel(intention_tsvector, intention_id) ' \
                    + 'select to_tsvector(%s), (select intention_id from intentions '\
                    + 'where intention_name = %s) '                                  \
                    + 'where not exists(select 1 from intentions_rel where intention_tsvector' \
                    + ' = to_tsvector(%s))', (call, name, call))
    cur.close()
    conn.commit()
