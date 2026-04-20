# password

> password(length: int = 12, special_chars: bool = True, upper_case: bool = False, lower_case: bool = False) -> str

Generate a random password.

**Arguments**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `length` | int | 12 | Number of characters in the password. Defaults to 12. |
| `special_chars` | bool | True | Include special characters (!@#...). Defaults to True. |
| `upper_case` | bool | False | Ensure at least one character is in uppercase. Defaults to False. |
| `lower_case` | bool | False | Ensure at least one character is in lowercase. Defaults to False. |

**Returns** `str`
