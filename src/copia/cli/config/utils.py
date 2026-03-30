def is_valid_hostname(host: str) -> bool:
    if len(host) > 253:
        return False
    labels = host.rstrip(".").split(".")
    for label in labels:
        if not label or len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        if not all(char.isalnum() or char == "-" for char in label):
            return False
    return True

def is_ascii_only(value: str) -> bool:
    return value.isascii()