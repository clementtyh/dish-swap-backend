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


class InvalidPasswordException(Exception):
    def __init__(self, message="Invalid password"):
        self.message = message
        super().__init__(self.message)
        

class DisplayNameExistException(Exception):
    def __init__(self, display_name):
        self.display_name = display_name
        super().__init__(f"Display name {self.display_name} already exists")


class UserNotFoundException(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"User with email '{self.email}' not found")


class UserIdNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"User id not found")

class InvalidUserIDException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"User ID '{id}' is invalid")