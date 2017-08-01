#!/bin/usr/python3.5
"""
Starting module for the docbot application
This application will be a slack (initially) bot to query \
information related to wathever is asked \
by the user
"""
import sys
from app.config import configmanager

def print_options():
    """
    Function utilized to print possible \
    commandline options for this application \
    """
    print('----------    Documentation bot    ----------')
    print('---------------------------------------------')
    print('The application must be executed with at     ')
    print('least one argument, accepted arguments are:  ')
    print('help      - shows this information pannel    ')
    print('make      - checks if config file exists     ')
    print('                 generating an default file  ')
    print('                 if it doesn\'t              ')
    print('makedb    - checks if the configured database')
    print('                 has the necessary tables and')
    print('                 is built correctly          ')
    print('startbot  - starts the bot                   ')

def main():
    """
    Main code entrance
    """
    if len(sys.argv) < 2:
        print_options()
        sys.exit(0)
    elif 'startbot' in sys.argv:
        print('Bot is starting')
    elif 'make' in sys.argv:
        has_config = configmanager.check_config()
        if has_config:
            print('.ini file already exists')
            conf = input('Would you like to replace it for a default .ini? (y/N)')
            while True:
                if conf == 'y' or conf == 'Y':
                    configmanager.fill_default()
                    configmanager.save_config()
                    break
                elif conf == 'n' or conf == 'N' or conf == '':
                    print('.ini file exists and wasn\'t altered')
                    break
                else:
                    conf = input('Please input either y or n')
        else:
            configmanager.make_config()
    elif 'makedb' in sys.argv:
        print('Veryfing db and creating necessary tables')
    elif 'help' in sys.argv:
        print_options()
    else:
        print('Unknown command, use argument help to see all commands')

if __name__ == '__main__':
    main()
else:
    print('This module should always run standalone')