class UserNotRegisteredException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class UserLockoutException(Exception):
    pass


class PasswordTooShortException(Exception):
    pass


class PasswordNotStrongEnoughException(Exception):
    pass


class InvalidPhoneNumberException(Exception):
    pass
