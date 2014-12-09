#!/usr/bin/env python

import sys
import logging
from squid_dynamodb.providers.dynamodb import DynamoDbAuthInfoProvider
from squid_dynamodb.providers.ec2 import Ec2AuthInfoProvider


class AclHelper(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.proxy_config_table = DynamoDbAuthInfoProvider()
        self.ec2_auth = Ec2AuthInfoProvider()

    def is_valid_request(self, request_metadata):
        if not request_metadata:
            return False

        try:
            username = self.ec2_auth.get_stack_name_for_private_ip(request_metadata['source_ip'])
            user_config = self.proxy_config_table.get_user_config(username)

            # TODO: not enough, there should be a string matching including wildcard support for *.google.de f.e.
            if request_metadata['host'] in user_config.get('URLs'):
                return True
            else:
                return False

        except Exception as e:
            self.logger.error("Could not get config from dynamodb. Error was: {0}".format(str(e)))
            return False

    #TODO: implementation needed parsing line and extracting a dict with request, host, source_ip
    def parse_request_metadata(self, line):
        pass

    def main_loop(self):
        while True:
            line = sys.stdin.readline()
            line = line.strip()

            request_metadata = self.parse_request_metadata(line)

            if self.is_valid_request(request_metadata):
                self.write_ok()
            else:
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
    aclhelper = AclHelper()
    aclhelper.main_loop()