class User:
    username: str
    password: str
    access_level: int

    def __init__(self, username: str, password: str, access_level: int):
        pass


class SecurityHandler:
    def handle_request(self, user: User):
        pass


class NoneSecurityHandler(SecurityHandler):
    def handle_request(self, user: User):
        pass


class SecurityHandlerChainPart(SecurityHandler):
    next_security_handler: SecurityHandler

    def set_next(self, next_handler: SecurityHandler):
        pass

    def handle_request(self, user: User):
        pass


class AuthenticationHandler(SecurityHandlerChainPart):
    __valid_credentials: dict

    def handle_request(self, user: User):
        pass


class AuthorizationHandler(SecurityHandlerChainPart):
    __minimum_access_level: int

    def handle_request(self, user: User):
        pass


class AuditHandler(SecurityHandlerChainPart):
    def handle_request(self, user: User):
        pass
    
