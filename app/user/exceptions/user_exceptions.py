

class UserNotRegisteredException(Exception):
    """
    Exception for user not registered
    """


class InvalidCredentialsException(Exception):

    """
    Raised when credentials are invalid.
    """

    attempt_count = 0

    def __init__(self, count=0):
        self.attempt_count = count
        super().__init__(count)


class UserLockoutException(Exception):
    """
    Raised when user is locked
    """


class PasswordTooShortException(Exception):
    """
    Raised when password is less than 8 characters
    """


class PasswordNotStrongEnoughException(Exception):
    """
    Raised when password does not contain alphanumeric and special characters
    """


class InvalidPhoneNumberException(Exception):
    """
    Raised when phone number is invalid
    """
