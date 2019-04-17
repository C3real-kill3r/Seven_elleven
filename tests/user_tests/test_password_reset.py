from tests.base_test import GraphQLTestCase
from test_fixtures.authentication.users_fixture import (
    password_reset_mutation,
    registration_query
)


class TestPasswordReset(GraphQLTestCase):
    def test_reset_password_success(self):
        self.query(registration_query, op_name='registerUser')
        resp = self.query(password_reset_mutation, op_name='resetPasswrord')
        self.assertIn("Check your email to get the reset link", str(resp))

    def test_reset_password_failure(self):
        resp = self.query(password_reset_mutation, op_name='resetPasswrord')
        self.assertIn("The email provided is incorrect, try again", str(resp))
