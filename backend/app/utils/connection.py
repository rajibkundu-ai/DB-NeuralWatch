from typing import Optional, Tuple


def _clean_value(value: str) -> str:
    if value.lower().startswith("tcp:"):
        return value[4:]
    return value


def extract_connection_details(connection_string: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (host, database) tuple parsed from an ODBC connection string."""
    if not connection_string:
        return None, None

    components = [segment.strip() for segment in connection_string.split(";") if segment.strip()]
    values = {}
    for component in components:
        if "=" not in component:
            continue
        key, value = component.split("=", 1)
        values[key.strip().lower()] = _clean_value(value.strip())

    host = (
        values.get("server")
        or values.get("data source")
        or values.get("addr")
        or values.get("address")
    )
    database = values.get("database") or values.get("initial catalog")

    return host, database
