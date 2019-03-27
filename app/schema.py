import graphene
import app.sevenelleven.authentication.schema


class Query(app.sevenelleven.authentication.schema.Query, graphene.ObjectType):
    pass


class Mutation(app.sevenelleven.authentication.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
