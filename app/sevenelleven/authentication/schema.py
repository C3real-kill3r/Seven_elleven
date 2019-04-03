import graphene
from graphql import GraphQLError

from graphql_extensions.auth.decorators import login_required
from graphene_django.types import DjangoObjectType
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, )

from app.sevenelleven.validations.validators import ErrorHandler
from .models import User as UserModel
from ..helpers.email_helpers import Email
from django.core.mail import send_mail


class Users(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(object):
    all_users = graphene.List(Users)

    @login_required
    def resolve_all_users(self, info, **kwargs):
        users = UserModel.objects.all()
        if users.count() == 0:
            raise GraphQLError("Users model is empty")
        return users


class RegisterUser(graphene.Mutation):
    """Mutation to register user"""
    user = graphene.Field(Users)

    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    def mutate(self, info, **kwargs):
        ErrorHandler().validate_empty_fields(**kwargs)
        ErrorHandler().validate_email(kwargs['email'])
        ErrorHandler().validate_password(kwargs['password'])
        user = UserModel(
            username=kwargs['username'],
            email=kwargs['email'],
        )

        if UserModel.objects.filter(username=kwargs['username']).exists():
            raise GraphQLError("Username already exists")
        elif UserModel.objects.filter(email=kwargs['email']).exists():
            raise GraphQLError("Email already exists")
        user.set_password(kwargs['password'])
        user.save()
        Email().send_account_activation_email(user)

        return RegisterUser(user=user)


class LogIn(graphene.Mutation):
    """
    Mutation to login a user
    """

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(Users)

    def mutate(self, info, email, password):
        user = {'email': email, 'password': password}
        serializer = JSONWebTokenSerializer(data=user)
        if serializer.is_valid():
            token = serializer.object['token']
            user = serializer.object['user']
            return LogIn(success=True, user=user, token=token, errors=None)
        else:
            raise GraphQLError(
                "The password and username dont match, try again")


class DeleteUser(graphene.Mutation):
    """Mutation to delete a user"""
    user = graphene.Field(Users)

    class Arguments:
        username = graphene.String(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        del_user = UserModel.objects.filter(
            username=kwargs['username']).first()
        if not del_user:
            raise GraphQLError(kwargs['username'] + " does not exist")
        else:
            del_user.delete()
            return DeleteUser(user=del_user)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    delete_user = DeleteUser.Field()
    log_in = LogIn.Field()
