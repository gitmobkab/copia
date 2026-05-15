def get_dict_values_as_str(dict_input: dict) -> str:
    values = dict_input.values()
    printable_values = map(lambda x: str(x), values)
    return ", ".join(printable_values)