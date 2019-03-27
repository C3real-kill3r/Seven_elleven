import re
from graphql import GraphQLError


class ErrorHandler():
    '''Handles errors in the application'''

    def validate_empty_fields(self, **kwargs):
        """
        Function to validate empty fields when
        saving an object
        :params kwargs
        """
        for field in kwargs:
            value = kwargs.get(field)
            if not type(value) is bool and not value.strip():
                raise AttributeError(field + " is required field")

    def validate_email(self, email):
        if re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                    email) is None:  # noqa
                    raise GraphQLError("The email is invalid!")

    def validate_password(self, password):  # noqa
        while True:
            if len(password) < 8:
                raise GraphQLError(
                    "Make sure your password is at lest 8 letters")
            elif re.search('[0-9]', password) is None:
                raise GraphQLError(
                    "Make sure your password has a number in it")
            elif re.search('[A-Z]', password) is None:
                raise GraphQLError(
                    "Make sure your password has capital letters in it")
            elif re.search('[\'$\',\'@\',\'#\']', password) is None:
                raise GraphQLError(
                    "Make sure your password has a special characters in it")
            else:
                break

# class PasswordEnryption():
#     """
