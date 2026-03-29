from pydantic import BaseModel, Field, StringConstraints
from typing import Literal

from typing import Annotated

from .globals import SUPPORTED_ADAPTERS, PORT_MIN_VAL, PORT_MAX_VAL

NotEmptyStr = Annotated[str, StringConstraints(
    True,
    min_length=1
)]

Port = Annotated[int, Field(
    ge= PORT_MIN_VAL,
    le= PORT_MAX_VAL,
    strict=True
)]


class Profile(BaseModel):
    adapter: SUPPORTED_ADAPTERS
    host: NotEmptyStr
    port: Port
    database: NotEmptyStr
    user: str
    password: str = ""
    
    
    def __str__(self) -> str:
        return f"({self.adapter}) <{self.host}:{self.port}>"

    def __repr__(self) -> str:
        return self.__str__()

PROFILE_DEFAULTS: dict[str, str] = {
    "adapter": "mysql",
    "host": "localhost",
    "port": "3306",
    "database": "",
    "user": "",
    "password": ""
}