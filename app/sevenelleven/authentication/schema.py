import graphene
from graphql import GraphQLError

from graphene_django.types import DjangoObjectType

from app.sevenelleven.validations.validators import ErrorHandler
from .models import User as UserModel


class Users(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(object):
    all_users = graphene.List(Users)

    def resolve_all_users(self, info, **kwargs):
        users = UserModel.objects.all()
        if users.count() == 0:
            raise GraphQLError("Users model is empty")
        return users


class RegisterUser(graphene.Mutation):
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
        return RegisterUser(user=user)


class DeleteUser(graphene.Mutation):
    user = graphene.Field(Users)

    class Arguments:
        username = graphene.String(required=True)

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
