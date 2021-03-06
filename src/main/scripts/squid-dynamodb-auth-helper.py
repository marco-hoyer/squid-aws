#!/usr/bin/env python

# validates a given request by:
# - validating basic_auth credentials, given from squid, against dynamodb proxy_config table entries

from squid_dynamodb.basic_auth_helper import DynamoDbAuthHelper

if __name__ == "__main__":
    authhelper = DynamoDbAuthHelper()
    authhelper.main_loop()