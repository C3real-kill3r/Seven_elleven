import graphene
import app.seveneleven.authentication.schema
import app.seveneleven.profiles.schema


class Query(
    app.seveneleven.authentication.schema.Query,
    app.seveneleven.profiles.schema.Query, graphene.ObjectType):  # noqa
    pass


class Mutation(
    app.seveneleven.authentication.schema.Mutation,
    app.seveneleven.profiles.schema.Mutation, graphene.ObjectType):  # noqa
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
