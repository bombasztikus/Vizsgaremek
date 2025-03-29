from typing import Self
from .models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AccessToken:
    """
    Represents an access token for a user.
    """

    def __init__(self, encoded_token: str, expiry: int) -> None:
        """
        Constructs a new AccessToken object.

        :param encoded_token: The encoded JWT token.
        :param expiry: The expiry time of the token in seconds.
        """

        self.encoded_token = encoded_token
        self.expiry = expiry

    def to_dto(self) -> dict:
        """"
        Converts the AccessToken object to a dictionary.

        :return: A dictionary representation of the AccessToken object.
        """

        return {
            "access_token": str(self.encoded_token),
            "expiry": int(self.expiry),
            "is_error": False
        }

    @staticmethod
    def from_user(user: User) -> Self:
        """
        Creates a new AccessToken from a User object.

        :param user: The User object.
        :return: An AccessToken object.
        """

        expiry_in_seconds = timedelta(days=30)
        token = create_access_token(
            user,
            expires_delta=expiry_in_seconds,
            additional_claims={
                "role": "admin" if user.is_employee else "user",
            }
        )

        return AccessToken(
            encoded_token=token,
            expiry=int(expiry_in_seconds.total_seconds())
        )
    
class AuthenticationHandler:
    """
    Handles authentication for users.
    """

    @staticmethod
    def flow_JWT(email: str, password: str) -> AccessToken:
        """
        Handles the authentication flow.
        Retrieves the user by email and password, and generates an access token.
        
        :param email: The user's email.
        :param password: The user's password.
        :return: An AccessToken object.
        """

        user = User.verify(
            email=email,
            password=password
        )

        return AccessToken.from_user(
            user=user
        )