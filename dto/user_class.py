import os
from typing import List
import requests

from utils.logger.logger import log_request, log_response


class User:
    """
    Represents a user with attributes such as email, first name, last name, and optional details and corresponding getters.
    The User class is designed to encapsulate user-related information and provide methods to access these attributes.

    Attributes:
        id (int): The unique identifier of the user. Defaults to None.
        email (str): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        avatar (str): The URL of the user's avatar. Defaults to None.
    """
    def __init__(self, email: str = None, first_name: str = None, last_name: str = None, id: int = None, avatar: str = None, job: str = None, createdAt: str = None):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.avatar = avatar

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_avatar(self):
        return self.avatar
    
    def set_id(self, id: int):
        self._id = id
        return self

    def set_email(self, email: str):
        self._email = email
        return self

    def set_first_name(self, first_name: str):
        self._first_name = first_name
        return self

    def set_last_name(self, last_name: str):
        self._last_name = last_name
        return self

    def set_avatar(self, avatar: str):
        self._avatar = avatar
        return self
    
    def __repr__(self):
        return (f"User(id={self.id}, email='{self.email}', first_name='{self.first_name}', "
                f"last_name='{self.last_name}', avatar='{self.avatar}'")
    
    def fetch_users(self, page=2, expectedStatusCode=200) -> List['User']:
        """
        Fetches a list of users from the API.

        This function sends a GET request to the API endpoint specified by the
        "BASE_URL" environment variable and retrieves a paginated list of users
        from page 2. It asserts that the response status code is 200 and parses
        the JSON response to create a list of User objects.

        Returns:
            List[User]: A list of User objects retrieved from the API.

        Raises:
            AssertionError: If the response status code is not 200.
            KeyError: If the expected "data" key is missing in the JSON response.
            JSONDecodeError: If the response body is not valid JSON.
        """
        url = f"{os.getenv('BASE_URL')}/users?page={page}"
        log_request("POST", url)
        response = requests.get(f"{os.getenv('BASE_URL')}/users?page={page}")
        log_response(response)
        
        if response.status_code != expectedStatusCode:
            raise ValueError(f"Unexpected status code: {response.status_code}")
        assert response.status_code == expectedStatusCode
        data = response.json()
        users = [User(**user) for user in data["data"]]
        return users
