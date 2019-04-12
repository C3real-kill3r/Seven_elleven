from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.serializers import UidAndTokenSerializer, PasswordRetypeSerializer
from djoser import utils
from graphql import GraphQLError

User = get_user_model()


class UidAndTokenSerializer(UidAndTokenSerializer):

    def validate_uid(self, value):
        try:
            uid = utils.decode_uid(value)
            self.user = User.objects.get(username=uid)
        except (
                User.DoesNotExist,
                ValueError,
                TypeError,
                OverflowError
                ) as error:
            raise GraphQLError("Invalid uid")
        return value

    def validate(self, attrs):
        self.validate_uid(attrs['uid'])
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise GraphQLError("Invalid token")
        return attrs


class PasswordResetConfirmRetypeSerializer(
        UidAndTokenSerializer, PasswordRetypeSerializer
        ):
    def validate(self, attrs):
        attrs = super(PasswordResetConfirmRetypeSerializer, self)\
            .validate(attrs)
        if attrs['new_password'] != attrs['re_new_password']:
            raise GraphQLError("The password entered do not match")
        return attrs
