class Handler:
    def init(self):
        self._next_handler = None

    def set_next_handler(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class AuthenticationHandler(Handler):
    def handle(self, request):
        if request.get("username") == "admin" and request.get("password") == "password":
            print("Authentication successful")
            return super().handle(request)
        print("Authentication failed")
        return {"status": "error", "message": "Invalid username or password"}


class AuthorizationHandler(Handler):
    def handle(self, request):
        if request.get("role") == "admin":
            print("Authorization successful")
            return super().handle(request)
        print("Authorization failed")
        return {"status": "error", "message": "Insufficient privileges"}


class AuditHandler(Handler):
    def handle(self, request):
        print("Audit record created")
        return {"status": "success"}


if name == "main":
    authentication_handler = AuthenticationHandler()
    authorization_handler = AuthorizationHandler()
    audit_handler = AuditHandler()

    authentication_handler.set_next_handler(authorization_handler).set_next_handler(audit_handler)

    # Test case 1: Authentication and authorization success
    request = {"username": "admin", "password": "password", "role": "admin"}
    result = authentication_handler.handle(request)
    print(result)

    # Test case 2: Authentication failed
    request = {"username": "user", "password": "password", "role": "admin"}
    result = authentication_handler.handle(request)
    print(result)

    # Test case 3: Authorization failed
    request = {"username": "admin", "password": "password", "role": "user"}
    result = authentication_handler.handle(request)
    print(result)