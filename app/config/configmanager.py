"""
Module responsible for creating, loading and mantaining \
the application ini file
"""
import os
import json
import configparser

class ConfigManager:
    """
    Singleton responsible for loading and maintaining the ini file
    """
    _config = None

    @staticmethod
    def get_manager():
        """
        Get class current instance or instantiate if \
        theres none
        """
        if ConfigManager._config is None:
            ConfigManager._config = ConfigManager()
            ConfigManager._config.load_config()
        return ConfigManager._config

    def __init__(self):
        self.cur_config = None

    def load_config(self):
        """
        Load the application ini file
        """
        if self.check_config():
            self.cur_config = configparser.ConfigParser()
            self.cur_config.read('.ini')


    def get_param(self, section, param, aslist=False):
        """
        Get parameter from config file based on section and parameter name
        """
        if section in self.cur_config:
            if param in self.cur_config[section]:
                if not aslist:
                    return self.cur_config.get(section, param)

                return json.loads(self.cur_config.get(section, param))

        return None

    def set_param(self, section, param, value):
        """
        Set parameter on config file based on section and parameter name
        """
        self.cur_config.set(section, param, value)

    def make_config(self):
        """
        Generates an default config file with necessary params
        """
        self.cur_config = configparser.ConfigParser()
        #Data Base related configuration
        self.cur_config['DBDATA'] = {'Host': '',                        \
                                   'User': '',                          \
                                   'Password': '', ''                   \
                                   'maxconnections': '5'}
        #Slack bot related configuration
        self.cur_config['SLACKDATA'] = {'BotId': '',                        \
                                   'BotToken': ''}
        self.cur_config['IO'] = {'inputmodule': 'app.io.consoleinput',      \
                                   'outputmodule': 'app.io.consoleoutput'}
        self.cur_config['INSTALLEDMODULES'] = {'InstalledModules': '[]'}
        self.save_config()

    def check_config(self):
        """
        Check if configuration file exists
        """
        if self.cur_config is None:
            exist = os.path.exists(os.getcwd() + '/.ini')
        else:
            exist = True
        return exist

    def save_config(self):
        """
        Check if configuration file exists
        """
        with open('.ini', 'w') as configfile:
            self.cur_config.write(configfile)
