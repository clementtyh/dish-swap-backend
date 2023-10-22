class UserAlreadyExistsException(Exception):
    def __init__(self, message="User with the given email or display name already exists"):
        self.message = message
        super().__init__(self.message)


class PasswordsDoNotMatchException(Exception):
    def __init__(self, message="Password and confirmation password must be the same"):
        self.message = message
        super().__init__(self.message)


class PasswordsMatchException(Exception):
    def __init__(self, message="Current password and new password cannot be the same"):
        self.message = message
        super().__init__(self.message)


class PasswordDoesNotMatchDatabaseException(Exception):
    def __init__(self, message="Provided password does not match"):
        self.message = message
        super().__init__(self.message)
        

class UserNotFoundException(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"User with email '{email}' not found")


class UserIdNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"User id not found")