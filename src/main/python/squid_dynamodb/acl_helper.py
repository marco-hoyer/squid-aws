#!/usr/bin/env python

import sys
import logging
import re
from squid_dynamodb.providers.dynamodb import DynamoDbAuthInfoProvider
from squid_dynamodb.providers.ec2 import Ec2AuthInfoProvider


class Ec2DynamodbAclHelper(object):

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
            if not user_config:
                return False

            return self.is_allowed_request(user_config.get('URLs'), request_metadata['dest_url'])

        except Exception as e:
            self.logger.error("Could not validate request: {0}".format(str(e)))
            return False

    def is_allowed_request(self, url_acls, dest_url):
        for url_acl in url_acls:
            if re.compile(url_acl).match(dest_url):
                return True

        return False

    # requires tag output format to be "0 sourceip dest_url"
    def parse_request_metadata(self, line):
        assert line, "Nothing parseable supplied, got blank newline!"
        request_metadata = {}

        item_list = line.split(" ")
        assert(len(item_list) >= 3), "Error parsing request-metadata from squid output, invalid format supplied!"

        request_metadata['source_ip'] = item_list[1].strip()
        request_metadata['dest_url'] = item_list[2].strip()
        return request_metadata

    def main_loop(self):
        while True:
            line = sys.stdin.readline()
            line = line.strip()
            assert line, "Nothing parseable supplied, got blank newline!"

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

    @staticmethod
    def write_unknown():
        sys.stdout.write('BH\n')
        sys.stdout.flush()

if __name__ == '__main__':
    aclhelper = Ec2DynamodbAclHelper()
    aclhelper.main_loop()