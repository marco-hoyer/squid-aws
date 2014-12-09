#!/usr/bin/env python

# validates a given request by:
# - looking up the cloudformation-stack-name for requests source-ip by ec2 api,
# - querying the allowed urls for the cloudformation-stack-name from dynamodb proxy_config table
# - matching host and scheme from request against allowed urls list from dynamodb

from squid_dynamodb.acl_helper import Ec2DynamodbAclHelper

if __name__ == "__main__":
    aclhelper = Ec2DynamodbAclHelper()
    aclhelper.main_loop()