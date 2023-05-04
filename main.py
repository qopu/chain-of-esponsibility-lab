class User:
    username: str
    password: str
    access_level: int

    def __init__(self, username: str, password: str, access_level: int):
        self.access_level = access_level
        self.password = password
        self.username = username


class SecurityHandler:
    def handle_request(self, user: User) -> None:
        raise NotImplementedError()


class SecurityHandlerChainPart(SecurityHandler):
    __next_security_handler: SecurityHandler

    def __init__(self):
        self.__next_security_handler = NoneSecurityHandler()

    def set_next(self, next_handler: SecurityHandler) -> None:
        self.__next_security_handler = next_handler

    def handle_request(self, user: User) -> None:
        return self.__next_security_handler.handle_request(user=user)


class NoneSecurityHandler(SecurityHandler):
    def handle_request(self, user: User):
        return "Доступ разрешён!"


class AuthenticationHandler(SecurityHandlerChainPart):
    __valid_credentials: dict = {"user": "user",
                                 "admin": "admin"}

    def handle_request(self, user: User):
        is_user_valid = user.username in self.__valid_credentials and \
                        user.password == self.__valid_credentials[user.username]
        if is_user_valid:
            return super().handle_request(user=user)
        return "Ошибка аутентификации"


class AuthorizationHandler(SecurityHandlerChainPart):
    __minimum_access_level: int = 3

    def handle_request(self, user: User):
        is_user_authorized = self.__minimum_access_level < user.access_level
        if is_user_authorized:
            return super().handle_request(user=user)
        return "Ошибка авторизации"


class AccountingHandler(SecurityHandlerChainPart):
    def handle_request(self, user: User):
        with open("logs.txt", "a") as file:
            file.writelines(f"User \"{user.password}\" authorized with access level {user.access_level}\n")
        return super().handle_request(user=user)


def do_tests():
    valid_user = User(username="user",
                      password="user",
                      access_level=4)
    invalid_user = User(username="hacker",
                        password="iWantToGetAccessSoBad",
                        access_level=5)
    low_access_user = User(username="user",
                           password="user",
                           access_level=1)
    admin = User(username="admin",
                 password="admin",
                 access_level=999)

    authentication = AuthenticationHandler()
    authorization = AuthorizationHandler()
    accounting = AccountingHandler()

    authentication.set_next(authorization)
    authorization.set_next(accounting)

    print(f"Valid user: {authentication.handle_request(user=valid_user)}")
    print(f"Invalid user: {authentication.handle_request(user=invalid_user)}")
    print(f"User with low access level: {authentication.handle_request(user=low_access_user)}")
    print(f"Admin: {authentication.handle_request(user=admin)}")


if __name__ == '__main__':
    do_tests()
