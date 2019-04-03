import graphene
import app.seveneleven.authentication.schema


class Query(app.seveneleven.authentication.schema.Query, graphene.ObjectType):
    pass


class Mutation(app.seveneleven.authentication.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
