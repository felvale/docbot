#!/usr/bin/python3
"""
Starting module for the docbot application
This application will be a slack (initially) bot to query \
information related to wathever is asked \
by the user
"""
import sys
from app.config.configmanager import ConfigManager
from app.db import makedb

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
    print('new-inten - prompts for data to create a new ')
    print('                 intention to the program    ')
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
        confman = ConfigManager.get_manager()
        has_config = confman.check_config()
        if has_config:
            print('.ini file already exists')
            conf = input('Would you like to replace it for a default .ini? (y/N):')
            while True:
                if conf == 'y' or conf == 'Y':
                    confman.make_config()
                    confman.save_config()
                    break
                elif conf == 'n' or conf == 'N' or conf == '':
                    print('.ini file exists and wasn\'t altered')
                    break
                else:
                    conf = input('Please input either y or n')
        else:
            print('Config file not found! Generating default file')
            confman.make_config()
    elif 'new-inten' in sys.argv:
        print('Creating intent')
    elif 'make-db' in sys.argv:
        print('Building db')
    elif 'help' in sys.argv:
        print_options()
    else:
        print('Unknown command, use argument help to see all commands')

if __name__ == '__main__':
    main()
else:
    print('This module should always run standalone')
