# ipv4

> ipv4(network: bool = False, address_class: Literal['a', 'b', 'c'] = 'c', private: bool = False) -> str

Generate a random IPv4 address.

**Arguments**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `network` | bool | False | Return a network address with CIDR notation (e.g. 192.168.0.0/24). |
| `address_class` | Literal['a', 'b', 'c'] | 'c' | IP address class to generate ('a', 'b', or 'c'). |
| `private` | bool | False | Restrict to private address ranges. Defaults to False. |

**Returns** `str`
