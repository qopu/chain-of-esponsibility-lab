class User:
    username: str
    password: str
    access_level: int

    def __init__(self, username: str, password: str, access_level: int):
        self.access_level = access_level
        self.password = password
        self.username = username


class SecurityHandler:
    def __init__(self):
        pass

    def handle_request(self, user: User) -> None:
        raise NotImplementedError()

class SecurityHandlerChainPart(SecurityHandler):
    __next_security_handler: SecurityHandler

    def set_next(self, next_handler: SecurityHandler) -> None:
        self.__next_security_handler = next_handler

    def handle_request(self, user: User) -> None:
        return self.__next_security_handler.handle_request(user=user)

class NoneSecurityHandler(SecurityHandler):
    def handle_request(self, user: User) -> None:
        pass

class AuthenticationHandler(SecurityHandlerChainPart):
    __valid_credentials: dict = { "user": "user",
                                  "admin": "admin" }

    def handle_request(self, user: User) -> None:
        is_user_valid = user.username in self.__valid_credentials and \
                        user.password == self.__valid_credentials[user.username]
        if is_user_valid:
            return super().handle_request(user=user)
        return "Ошибка аутентификации"



class AuthorizationHandler(SecurityHandlerChainPart):
    __minimum_access_level: int

    def handle_request(self, user: User) -> None:
        is_user_authorized = self.__minimum_access_level < user.access_level
        if is_user_authorized:
            return super().handle_request(user=user)
        return "Ошибка авторизации"


class AuditHandler(SecurityHandlerChainPart):
    def handle_request(self, user: User) -> None:
        print(f"Пользователь {user} произвёл авторизацию")
        return super().handle_request(user=user)