import unittest2
from mock import patch, Mock
from squid_dynamodb import acl_helper

class AclHelperTest(unittest2.TestCase):

    def setUp(self):
        self.dynamoDbPatcher = patch("squid_dynamodb.acl_helper.DynamoDbAuthInfoProvider")
        self.ec2Patcher = patch("squid_dynamodb.acl_helper.Ec2AuthInfoProvider")
        self.dynamoDbPatcher.start()
        self.ec2Patcher.start()
        self.aclHelper = acl_helper.Ec2DynamodbAclHelper()

    def tearDown(self):
        self.dynamoDbPatcher.stop()
        self.ec2Patcher.stop()

    def test_disallowsIfUrlsDoNotMatch(self):
        self.assertFalse(self.aclHelper.is_allowed_request(['http://www.is24.de'], 'http://www.google.com'))


    def test_allows(self):
        self.assertTrue(self.aclHelper.is_allowed_request(['http://.*\.is24\.de'], 'http://www.is24.de'))