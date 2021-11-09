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
            if len(self.users) < 2:
                return False
            if not self.email.get_config():
                return False
            return True
        except IOError as error:
            logging.error('File not available: {}'.format(error))
        except KeyError as error:
            logging.error('Key not available: {}'.format(error))
        except TypeError as error:
            logging.error('Type not available: {}'.format(error))
        return False

    def get_html(self, user, to_give):
        '''Returns beautiful html for email'''
        logging.info('get_html()')
        html = '''<!DOCTYPE html>
            <html>
                <header>
                    <div style="background-color:#eee;padding:10px 20px;">
                        <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;"> Christmas 2021 - GCC International Mini Group</h2>
                    </div>
                </header
                <body>
                    <div style="padding:20px 0px">
                        <div style="height: 500px;width:400px">
                            <img src="https://act4.tv/wp-content/uploads/2020/11/SecretSanta-500.jpg" style="height: 300px;">
                            <div style="text-align:center;">
                                <h3>Secret Santa</h3>
                                <p>Hi {}</p>
                                <p>Your Secret Santa is:</p>
                                <h2>{}<h2>
                            </div>
                        </div>
                        <div>
                            <h3>Rules</h3>
                            <ul>
                                <li>You cannot spend more than £5</li>
                                <li>Please remember to keep this a secret</p>
                            </ul>
                        </div>
                    </div>
                </body>
                <footer>
                    <div>
                        <p>If you liked this and wanted to know how this was developed, I have included the source code:</p>
                        <a href="https://github.com/Rubber-Duck-999/Secret-Santa">Github</a>
                    </div>
                </footer>
            </html>
            '''.format(user, to_give)
        return html

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
            if user.to_give != user.name and len(user.to_give) > 0:
                logging.info('User: {}'.format(user.name))
                self.email.send(user.email, self.get_html(user.name, user.to_give))
            else:
                logging.info('User: {} has no valid give'.format(user.name))

if __name__ == "__main__":
    '''Entry point'''
    secret = SecretSanta()
    if secret.get_config():
        secret.create_users()