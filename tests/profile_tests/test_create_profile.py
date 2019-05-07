from tests.base_test import GraphQLTestCase
from test_fixtures.profile.profile_fixtures import (
    create_profile_query,
    get_profiles_query
)
from test_fixtures.authentication.users_fixture import (
    registration_query,
    login_query
)


class TestProfile(GraphQLTestCase):
    def test_create_profile(self):
        self.query(registration_query, op_name='registerUser')
        self.query(login_query, op_name='logIn')
        resp = self.query(
            create_profile_query, op_name='createProfile')
        self.assertIn("hello people", str(resp))

    def test_duplicate_profile_creation(self):
        self.query(registration_query, op_name='registerUser')
        self.query(login_query, op_name='logIn')
        self.query(create_profile_query, op_name='createProfile')
        resp2 = self.query(
            create_profile_query, op_name='createProfile')
        self.assertIn("The profile has already been created", str(resp2))

    def test_view_profiles(self):
        self.query(registration_query, op_name='registerUser')
        self.query(login_query, op_name='logIn')
        self.query(create_profile_query, op_name='createProfile')
        resp = self.query(get_profiles_query, op_name='allProfiles')
        self.assertIn("people", str(resp))

    def test_view_profiles_with_empty_profile_model(self):
        self.query(registration_query, op_name='registerUser')
        self.query(login_query, op_name='logIn')
        resp = self.query(get_profiles_query, op_name='allProfiles')
        self.assertIn("empty", str(resp))
