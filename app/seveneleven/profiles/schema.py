import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from .models import Profile as ProfileModel


class Profiles(DjangoObjectType):
    class Meta:
        model = ProfileModel


class Query(object):
    all_profiles = graphene.List(Profiles)

    def resolve_all_profiles(self, info, **kwargs):
        profiles = ProfileModel.objects.all()
        if profiles.count() == 0:
            raise GraphQLError("There profile model is empty")
        return profiles


class CreateProfile(graphene.Mutation):
    """Mutation to create a user profile"""
    profile = graphene.Field(Profiles)
    success = graphene.List(graphene.String)

    class Arguments:
        user_id = graphene.Int(required=True)
        image = graphene.String(required=True)
        bio = graphene.String(required=True)
        birth_date = graphene.String(required=True)
        location = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = ProfileModel.objects.filter(user_id=info.context.user.id).first()
        if not user:
            profile = ProfileModel(
                user_id=info.context.user.id,
                image=kwargs['image'],
                bio=kwargs['bio'],
                birth_date=kwargs['birth_date'], location=kwargs['location'])
            profile.save()
            return CreateProfile(profile=profile, success=["successfully created"])
        else:
            raise GraphQLError("The profile has already been created")


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
