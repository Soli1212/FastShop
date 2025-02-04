from fastapi import Response


def set_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: int = 3600,
    http_only: bool = True,
):
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        expires=max_age,
        httponly=http_only,
        # secure=True,
        samesite="Strict",
    )


def delete_cookie(response: Response, key: str):
    response.delete_cookie(key=key)
