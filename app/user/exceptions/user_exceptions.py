class UserNotRegisteredException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class UserLockoutException(Exception):
    pass
