#!/usr/bin/env python

from squid_dynamodb.auth_helper import DynamoDbAuthHelper

if __name__ == "__main__":
    authhelper = DynamoDbAuthHelper()
    authhelper.main_loop()