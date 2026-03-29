from typing import get_args, Any
from prompt_toolkit.document import Document
import questionary


from ..config.globals import SUPPORTED_ADAPTERS, PORT_MIN_VAL, PORT_MAX_VAL
from ..config.models import Profile, PROFILE_DEFAULTS

SUPPORTED_ADAPTERS_LIST = list(get_args(SUPPORTED_ADAPTERS))


class NotEmptyStrValidator(questionary.Validator):
    """
    A questionary validator that only validate strings with 3 or more characters
    
    **Note:** trailing whitespaces are not stripped from the verification
    """
    
    def validate(self, document: Document) -> None:
        if len(document.text) < 3:
            raise questionary.ValidationError(
                message="The string must have 3 or more characters",
                cursor_position=len(document.text)
            )
            
class PortValidator(questionary.Validator):
    """
    A questionary validator that ensure the string can be safely converted to a port
    
    which means an integer in the interval [PORT_MIN_VAL, PORT_MAX_VAL]
    
    the port limits are defined in the config.globals module
    """
    
    def validate(self, document: Document) -> None:
        try:
            value = int(document.text)
        except ValueError:
            raise questionary.ValidationError(
                message="Expected a valid integer",
                cursor_position=len(document.text)
            )
        if value not in range(PORT_MIN_VAL, PORT_MAX_VAL):
            raise questionary.ValidationError(
                message=f"Expected a value in [{PORT_MIN_VAL} ,{PORT_MAX_VAL}]",
                cursor_position=len(document.text)
            )
    
def profile_questionary(defaults: dict = {}) -> Profile:
    
    real_defaults = get_profile_defaults(defaults)
    
    form = questionary.form(
        adapter = questionary.select("select the profile_data adapter", 
                                 SUPPORTED_ADAPTERS_LIST,
                                 default=real_defaults["adapter"],
                                 show_selected=True),
        
        host = questionary.text("type the host (localhost, 127.0.1.1, etc)",
                            default=real_defaults["host"],
                            validate=NotEmptyStrValidator),
        
        port = questionary.text("type the port to use",
                            default=real_defaults["port"],
                            validate=PortValidator),
        
        database = questionary.text("type the name of the database used by the profile_data",
                                    default=real_defaults["database"],
                                    validate=NotEmptyStrValidator),
    
        user = questionary.text("type the username to use for db connexion",
                            default=real_defaults["user"]),
    
        password = questionary.password("the password to use to connect",
                                    default=real_defaults["password"])
    ).unsafe_ask()
    
    form["port"] = int(form["port"])
    return Profile(**form)

def get_profile_defaults(profile_data: dict = {}) -> dict[str, str]:
    defaults: dict[str, str] = {}
    
    for key, default_val in PROFILE_DEFAULTS.items():
        defaults[key] = profile_data.get(key, default_val)
    
    return ensure_dict_val_are_strings(defaults)

def ensure_dict_val_are_strings(dictionary: dict) -> dict[Any, str]:
    for key, value in dictionary.items():
        if isinstance(value, str):
            continue
        dictionary[key] = str(value)
    return dictionary