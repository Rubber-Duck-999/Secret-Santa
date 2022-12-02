import logging
from errors import BadData

class User:
    def __init__(self, user):
        self.user = user
        self.name = ''
        self.email = ''
        self.exclude = []
        self.to_give = ''

    def convert_user(self):
        valid_user = True
        try:
            self.name = self.user['name']
            if len(self.name) < 3:
                raise BadData('User was not correct name length')
            self.exclude = self.user['exclude']
        except KeyError as error:
            logging.error('Key error on conversion: {}'.format(error))
        except BadData:
            logging.error('Data in json was invalid')
            valid_user = False
        return valid_user