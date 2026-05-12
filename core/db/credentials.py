from typing import Any


class CredentialsRepo:
    def get_all(self, user: str) -> dict[str, Any]:
        raise NotImplementedError
