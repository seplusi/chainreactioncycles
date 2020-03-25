import configparser


class Config:

    def __init__(self, config_file='properties.ini'):
        self.config = configparser.ConfigParser()
        properties_file_path_lst = __file__.split('/')[:-1]
        properties_file_path = '/'.join(properties_file_path_lst)
        self.config.read('%s/properties.ini' % properties_file_path)
