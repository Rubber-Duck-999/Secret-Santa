import logging
import json
import random
import os
import time
from emailer import Emailer
from user import User

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

logging.info("Starting program")

class SecretSanta:
    '''Class to decide where to send info to users'''
    def __init__(self):
        self.config = 'config.json'
        self.email = Emailer(self.config)
        self.users = []
        self.done_list = []
        self.finished_users = []

    def get_config(self):
        '''Get configuration values'''
        logging.info('# get_config()')
        try:
            if not os.path.isfile(self.config):
                return False
            config_file = open(self.config, "r")
            config_data = json.load(config_file)
            self.users  = config_data["users"]
            if len(self.users) < 4:
                return False
            return True
        except IOError as error:
            logging.error('File not available: {}'.format(error))
        except KeyError as error:
            logging.error('Key not available: {}'.format(error))
        except TypeError as error:
            logging.error('Type not available: {}'.format(error))
        return False

    def random_number(self, retry):
        '''Get random number, retry if number matches retry'''
        valid = False
        while not valid:
            num = random.randint(0, len(self.users) - 1)
            if num in retry:
                logging.debug('Not correct, in retry list')
            elif num in self.done_list:
                logging.debug('Already found, retry')
            else:
                logging.debug('Success')
                valid = True
        return num

    def calculate_user(self, index, user):
        '''Work out the recipient from exclusion'''
        exclude_list = [index]
        for index, exclude_user in enumerate(self.users):
            if exclude_user.name in user.exclude:
                exclude_list.append(index)
        give_index = self.random_number(exclude_list)
        user.to_give = self.users[give_index].name
        self.finished_users.append(user)
        self.done_list.append(give_index)

    def create_users(self):
        logging.info('# create_users()')
        temp_users = []
        for user in self.users:
            new_user = User(user)
            if new_user.convert_user():
                temp_users.append(new_user)
        self.users = temp_users
        for index, user in enumerate(self.users):
            self.calculate_user(index, user)
        for index, user in enumerate(self.finished_users):
            logging.info('User: {} will send to: {}'.format(user.name, user.to_give))

if __name__ == "__main__":
    '''Entry point'''
    secret = SecretSanta()
    if secret.get_config():
        secret.create_users()