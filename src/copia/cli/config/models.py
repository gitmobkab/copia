from typing import Annotated, Union

from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from pydantic.networks import IPvAnyAddress

from .globals import Adapter, PORT_MIN_VAL, PORT_MAX_VAL


NotEmptyStr = Annotated[str, StringConstraints(
    min_length=1
)]

Port = Annotated[int, Field(
    ge= PORT_MIN_VAL,
    le= PORT_MAX_VAL,
    strict=True
)]

class Profile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    adapter: Adapter
    host: Union[IPvAnyAddress, NotEmptyStr]
    port: Port
    database: NotEmptyStr
    user: NotEmptyStr
    password: str = ""

        
    def __str__(self) -> str:
        return f"({self.adapter}) <{self.host}:{self.port}>"

    def __repr__(self) -> str:
        return self.__str__()

