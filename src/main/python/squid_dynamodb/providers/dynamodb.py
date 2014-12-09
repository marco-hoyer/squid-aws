from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.exception import NoAuthHandlerFound
from squid_dynamodb.utils import timed
import logging
import sys


class DynamoDbAuthInfoProvider(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        try:
            self.connection = DynamoDBConnection(host='dynamodb.eu-west-1.amazonaws.com', region='eu-west-1')
            self.proxy_config_table = Table('proxy_config', connection=self.connection)
        except NoAuthHandlerFound as e:
            self.logger.error("Could not authenticate against aws api: {0}".format(str(e)))
            sys.exit(1)
        except Exception as e:
            self.logger.error("Could not load configuration table from dynamodb: {0}".format(str(e)))

    @timed
    def get_user_config(self, user):
        return self.proxy_config_table.get_item(User=user)