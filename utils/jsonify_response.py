from fastapi.responses import Response


def json_response(msg: str, key: str = "message"):
    return {key: msg}
