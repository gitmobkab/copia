from typing import Annotated, Union

from pydantic import BaseModel, Field, StringConstraints
from pydantic.networks import IPvAnyAddress

from .globals import Adapter, PORT_MIN_VAL, PORT_MAX_VAL


NotEmptyStr = Annotated[str, StringConstraints(
    min_length=1
)]

Port = Annotated[int, Field(
    ge= PORT_MIN_VAL,
    le= PORT_MAX_VAL,
    strict=True,
    description="The Database Port"
)]
    
class BaseProfile(BaseModel):
    adapter: Adapter = Field(description="The copia Adapter to use")

class ServerBasedProfile(BaseProfile):
    
    host: Union[IPvAnyAddress, NotEmptyStr] = Field(description="The database hostname")
    port: Port
    database: NotEmptyStr = Field(description="The Database Port")
    user: NotEmptyStr = Field(description="The Database Username")
    password: str = Field("", description="The Database Password")

        
    def __str__(self) -> str:
        return f"({self.adapter}) <{self.host}:{self.port}>"

    def __repr__(self) -> str:
        return self.__str__()

class FileBasedProfile(BaseProfile):
    database: str
    
    def __str__(self) -> str:
        return f"{self.database}"

def resolve_profile(payload: dict) -> BaseProfile:
    basic_info = BaseProfile(**payload)
    if basic_info.adapter == "mysql":
        return FileBasedProfile(**payload)
    else:
        return ServerBasedProfile(**payload)
