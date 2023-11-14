from entities.user import User


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password):
        self.validate(username, password)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        # toteuta loput tarkastukset tänne ja nosta virhe virhetilanteissa

        if len(username) < 3:
            raise UserInputError("Username needs to be at least 3 characters long")
        
        for character in username:
            ascii_val = ord(character)
            if ascii_val > 122 or ascii_val < 97:
                raise UserInputError("Username should only contain characters a-z")

        if len(password) < 8:
            raise UserInputError("Password needs to be at least 8 characters long")
        
        non_letter_char = False
        for character in password:
            ascii_val = ord(character.lower())
            if ascii_val > 122 or ascii_val < 97:
                non_letter_char = True
        if not non_letter_char:
            raise UserInputError("Password can not be only letters")
