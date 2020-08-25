import unittest
import aws_account_details
from aws_account_details import get_aws_account_details


class TestAWSAccountDetails(unittest.TestCase):
    def test_alpha_syd_env(self):
        testEnvDetails = {
            'id': '568431661506',
            'name': 'alpha',
            'region': 'ap-southeast-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('dev'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('tech'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('migdev'))


    def test_alpha_nvirgina_env(self):
        testEnvDetails = {
            'id': '568431661506',
            'name': 'alpha',
            'region': 'us-east-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-dev'))


    def test_alpha_oregon_env(self):
        testEnvDetails = {
            'id': '568431661506',
            'name': 'alpha',
            'region': 'us-west-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('gl-dev'))


    def test_alpha_ireland_env(self):
        testEnvDetails = {
            'id': '568431661506',
            'name': 'alpha',
            'region': 'eu-west-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('eu-dev'))


    def test_beta_syd_env(self):
        testEnvDetails = {
            'id': '723236915308',
            'name': 'beta',
            'region': 'ap-southeast-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('qa'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('stg'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('qaload'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('tpi'))


    def test_beta_singapore_env(self):
        testEnvDetails = {
            'id': '723236915308',
            'name': 'beta',
            'region': 'ap-southeast-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('stg2'))


    def test_beta_nvirgini_env(self):
        testEnvDetails = {
            'id': '723236915308',
            'name': 'beta',
            'region': 'us-east-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-qa'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-stg'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-tpi'))


    def test_beta_oregon_env(self):
        testEnvDetails = {
            'id': '723236915308',
            'name': 'beta',
            'region': 'us-west-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('gl-qa'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('gl-stg'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('gl-tpi'))


    def test_beta_ireland_env(self):
        testEnvDetails = {
            'id': '723236915308',
            'name': 'beta',
            'region': 'eu-west-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('eu-qa'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('eu-stg'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('pentest'))


    def test_psi_syd_env(self):
        testEnvDetails = {
            'id': '687512651472',
            'name': 'psi',
            'region': 'ap-southeast-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('sbox'))


    def test_psi_nvirgini_env(self):
        testEnvDetails = {
            'id': '687512651472',
            'name': 'psi',
            'region': 'us-east-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-sbox'))


    def test_psi_oregon_env(self):
        testEnvDetails = {
            'id': '687512651472',
            'name': 'psi',
            'region': 'us-west-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('gl-sbox'))


    def test_psi_ireland_env(self):
        testEnvDetails = {
            'id': '687512651472',
            'name': 'psi',
            'region': 'eu-west-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('eu-sbox'))


    def test_omega_syd_env(self):
        testEnvDetails = {
            'id': '830726149330',
            'name': 'omega',
            'region': 'ap-southeast-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('prod'))


    def test_omega_singapore_env(self):
        testEnvDetails = {
            'id': '830726149330',
            'name': 'omega',
            'region': 'ap-southeast-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('prod2'))


    def test_omega_nvirgini_env(self):
        testEnvDetails = {
            'id': '830726149330',
            'name': 'omega',
            'region': 'us-east-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-prod'))


    def test_omega_oregon_env(self):
        testEnvDetails = {
            'id': '830726149330',
            'name': 'omega',
            'region': 'us-west-2'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('us-prod2'))
        self.assertDictEqual(testEnvDetails, get_aws_account_details('gl-prod'))


    def test_omega_ireland_env(self):
        testEnvDetails = {
            'id': '830726149330',
            'name': 'omega',
            'region': 'eu-west-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('eu-prod'))


    def test_omega_frankfurt_env(self):
        testEnvDetails = {
            'id': '830726149330',
            'name': 'omega',
            'region': 'eu-central-1'
        }

        self.assertDictEqual(testEnvDetails, get_aws_account_details('eu-prod2'))
