#!/usr/bin/env python

import sys
import logging
from boto.dynamodb2.exceptions import ItemNotFound
from squid_dynamodb.providers.dynamodb import DynamoDbAuthInfoProvider
from squid_dynamodb.utils import timed


class DynamoDbAuthHelper(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.proxy_config_table = DynamoDbAuthInfoProvider()

    @timed
    def get_user_config_from_dynamodb(self, username):
        try:
            return self.proxy_config_table.get_user_config(username)
        except ItemNotFound:
            self.logger.warn("User {0} not found!".format(username))
            return None
        except Exception as e:
            self.logger.error("Could not get config from dynamodb. Error was: {0}".format(str(e)))
            return None

    def validate_password(self, user_config, basic_auth_credentials):
        try:
            if user_config.get("Password") == basic_auth_credentials['password']:
                return True
            else:
                return False
                self.logger.warn("Invalid password supplied for user {0}".format(basic_auth_credentials['username']))
        except Exception as e:
            return False

    def parse_basic_auth_credentials(self, line):
        assert line, "Nothing parseable supplied, got blank newline!"
        basic_auth_credentials = {}

        item_list = line.split(" ")
        assert(len(item_list) == 2), "Error parsing basic-auth credentials from squid output, invalid format supplied!"

        basic_auth_credentials['username'] = item_list[0].strip()
        basic_auth_credentials['password'] = item_list[1].strip()
        return basic_auth_credentials

    def main_loop(self):
        while True:
            try:
                line = sys.stdin.readline()
                line = line.strip()

                basic_auth_credentials = self.parse_basic_auth_credentials(line)
                user_config = self.get_user_config_from_dynamodb(basic_auth_credentials['username'])

                if self.validate_password(user_config, basic_auth_credentials):
                    self.write_ok()
                else:
                    self.write_error()
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                self.logger.error("Couldn't validate credentials!")
                self.logger.exception(e)
                self.write_error()

    @staticmethod
    def write_ok():
        sys.stdout.write('OK\n')
        sys.stdout.flush()

    @staticmethod
    def write_error():
        sys.stdout.write('ERR\n')
        sys.stdout.flush()

if __name__ == '__main__':
    authhelper = DynamoDbAuthHelper()
    authhelper.main_loop()