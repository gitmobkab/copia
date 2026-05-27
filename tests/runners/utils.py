from copia.parser.models import Column, GeneratorCall, Params, POSITIONALS, NAMED

def make_column(generator: str,
                name: str | None = None,
                positionals: POSITIONALS = [],
                named: NAMED = {},
                unique: bool =False) -> Column:
    
    return Column(
        name=name,
        unique_constraint=unique,
        generator=GeneratorCall(
            name=generator,
            params=Params(
                positionals=positionals,
                named=named
            )
        )
    )