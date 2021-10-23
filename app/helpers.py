def filter_empty_keys(values: dict) -> dict:
    keys = list(values.keys())
    for key in keys:
        if values[key] is None:
            del values[key]
    return values
