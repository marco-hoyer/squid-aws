#!/data/home/mhoyer/virtualenv_2.6/bin/python

from squid_dynamodb.auth_helper import DynamoDbAuthHelper

if __name__ == "__main__":
    authhelper = DynamoDbAuthHelper()
    authhelper.main_loop()