import strawberry
from ..queries import Query


@strawberry.type
class Health:
    status: str


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> Health:
        return Health(status="ok")


schema = strawberry.Schema(query=Query)
