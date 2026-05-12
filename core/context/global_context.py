from dataclasses import dataclass


class DbConnection: ...


class AuthenticatedUser: ...


@dataclass(frozen=True)
class GlobalContext:
    db_connection: DbConnection
    current_user: AuthenticatedUser
