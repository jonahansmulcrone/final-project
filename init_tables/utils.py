def parse_int(value: str) -> int | None:
    """
    Parse a string into an integer, throwing if it's not a valid int, or None if it's an empty string
    """
    return int(value) if len(value) > 0 else None
