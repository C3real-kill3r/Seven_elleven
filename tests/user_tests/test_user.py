from tests.base_test import GraphQLTestCase
from test_fixtures.authentication.users_fixture import (
    registration_query,
    registration_wrong_password_query,
    registration_wrong_password_response,
    registration_wrong_email_query,
    login_query,
    login_wrong_password,
    delete_user_query,
    delete_non_existent_user_query,
    get_users_query,
)


class TestUser(GraphQLTestCase):
    def test_register_mutation_success(self):
        resp = self.query(
            registration_query, op_name='registerUser')
        self.assertIn("Check your email to activate your account", str(resp))

    def test_user_registration_incorrect_password(self):
        resp = self.query(
            registration_wrong_password_query, op_name='registerUser')
        self.assertEqual(resp, registration_wrong_password_response)

    def test_user_registration_incorrect_email_format(self):
        resp = self.query(
            registration_wrong_email_query, op_name='registerUser')
        self.assertIn("The email is invalid!", str(resp))

    def test_user_login_success(self):
        self.query(registration_query, op_name='registerUser')
        resp = self.query(login_query, op_name='logIn')
        self.assertIn("Rybczynski", str(resp))

    def test_user_login_failure(self):
        self.query(registration_query, op_name='registerUser')
        resp = self.query(login_wrong_password, op_name='logIn')
        self.assertIn("The password and username dont match, try again", str(resp))

    def delete_user_success(self):
        resp = self.query(delete_user_query, op_name='deleteUser')
        self.assertIn("brybzi@gmail", str(resp))

    def test_delete_user_failure(self):
        resp = self.query(delete_non_existent_user_query, op_name='deleteUser')
        self.assertIn("Rybczynsk does not exist", str(resp))

    def test_get_registred_users(self):
        self.query(registration_query, op_name='registerUser')
        resp = self.query(get_users_query, op_name='allUsers')
        self.assertIn("Rybczynski", str(resp))

    def test_get_registred_users_empty_model(self):
        resp = self.query(get_users_query, op_name='allUsers')
        self.assertIn("Users model is empty", str(resp))
