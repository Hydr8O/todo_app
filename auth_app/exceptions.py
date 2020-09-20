class PasswordMismatchException(Exception):
    def __init__(self):
        self.message = 'Passwords did not match'
    
    def __str__(self):
        return self.message

class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.message = 'User with this username already exists'
    
    def __str__(self):
        return self.message

class WrongCredentialsException(Exception):
    def __init__(self):
        self.message = 'Wrong username or password'
    
    def __str__(self):
        return self.message

class UserActivationException(Exception):
    def __init__(self):
        self.message = 'Tokens did not match'

    def __str__(self):
        return self.message