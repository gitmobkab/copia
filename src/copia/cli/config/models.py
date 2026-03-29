from typing import Annotated, Union

from pydantic import BaseModel, Field, StringConstraints, field_validator
from pydantic.networks import IPvAnyAddress

from .globals import SUPPORTED_ADAPTERS, PORT_MIN_VAL, PORT_MAX_VAL
from .utils import is_valid_hostname, is_ascii_only

NotEmptyStr = Annotated[str, StringConstraints(
    min_length=1
)]

Port = Annotated[int, Field(
    ge= PORT_MIN_VAL,
    le= PORT_MAX_VAL,
    strict=True
)]

PROFILE_DEFAULTS: dict[str, str] = {
    "adapter": "mysql",
    "host": "localhost",
    "port": "3306",
    "database": "",
    "user": "",
    "password": ""
}

_ADAPTERS_SCHEMES: dict[SUPPORTED_ADAPTERS, str] = {
    "mysql": "mysql+pymysql",
    "postgres": "postgresql+psycopg2",
}

class Profile(BaseModel):
    adapter: SUPPORTED_ADAPTERS
    host: Union[IPvAnyAddress, NotEmptyStr]
    port: Port
    database: NotEmptyStr
    user: NotEmptyStr
    password: str = ""
    
    class Config:
        extra = "forbid"
    
    @property
    def adapter_scheme(self) -> str:
        return _ADAPTERS_SCHEMES[self.adapter]
    
    @field_validator("host", mode="after")
    @classmethod
    def validate_host(cls, value: str) -> str:
        if isinstance(value, IPvAnyAddress):
            return value
        if is_valid_hostname(value):
            return value
        raise ValueError(f"Invalid host: {value!r}")
    
    @field_validator("database", "user", mode="after")
    @classmethod
    def validate_ascii_only_string(cls, value: str):
        if is_ascii_only(value):
            return value
        raise ValueError(f"The input must contains only ASCII chars, got {value!r}")
        
    def __str__(self) -> str:
        return f"({self.adapter}) <{self.host}:{self.port}>"

    def __repr__(self) -> str:
        return self.__str__()

