from boto.dynamodb2.exceptions import ItemNotFound
import unittest2
from mock import patch, Mock
from squid_dynamodb import basic_auth_helper

class AuthHelperTests(unittest2.TestCase):

    def setUp(self):
        self.patcher = patch("squid_dynamodb.auth_helper.DynamoDbAuthInfoProvider")
        self.authInfoProvider = self.patcher.start()
        self.authHelper = basic_auth_helper.DynamoDbAuthHelper()

    def tearDown(self):
        self.patcher.stop()

    def test_getUserConfig(self):
        self.authHelper.get_user_config_from_dynamodb("egal")
        self.authInfoProvider.return_value.get_user_config.assert_called_with("egal")

    def test_getUserConfigFailsWithItemNotFound(self):
        self.authInfoProvider.return_value.get_user_config.side_effect = ItemNotFound("bang!")
        self.assertEqual(self.authHelper.get_user_config_from_dynamodb("egal"), None)

    def test_validate_password(self):
        USER_CONFIG_MOCK = Mock()
        USER_CONFIG_MOCK.get.return_value = "testpassword"
        BASIC_AUTH_CREDENTIALS = {"username": "testuser", "password":"testpassword"}
        self.assertTrue(self.authHelper.validate_password(USER_CONFIG_MOCK, BASIC_AUTH_CREDENTIALS))

    def test_validate_password_returns_false_for_none_basic_auth_params(self):
        USER_CONFIG_MOCK = Mock()
        BASIC_AUTH_CREDENTIALS = {"username": None, "password":None}
        self.assertFalse(self.authHelper.validate_password(USER_CONFIG_MOCK, BASIC_AUTH_CREDENTIALS))

    def test_validate_password_returns_false_for_empty_basic_auth_param(self):
        USER_CONFIG_MOCK = Mock()
        BASIC_AUTH_CREDENTIALS = {}
        self.assertFalse(self.authHelper.validate_password(USER_CONFIG_MOCK, BASIC_AUTH_CREDENTIALS))

    def test_parse_basic_auth_credentials(self):
        RAW_STRING = "my-user pass123"
        EXPECTED = {"username": "my-user", "password":"pass123"}
        self.assertEqual(self.authHelper.parse_basic_auth_credentials(RAW_STRING),EXPECTED )

    def test_parse_basic_auth_credentials_raises_assertion_error_for_empty_string(self):
        RAW_STRING = ""
        with self.assertRaises(AssertionError):
            self.authHelper.parse_basic_auth_credentials(RAW_STRING)

    def test_parse_basic_auth_credentials_raises_assertion_error_for_single_element_string(self):
        RAW_STRING = "my-user"
        with self.assertRaises(AssertionError):
            self.authHelper.parse_basic_auth_credentials(RAW_STRING)
