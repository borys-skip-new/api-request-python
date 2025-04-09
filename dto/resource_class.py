import os
import requests


class Resource:
    """
    Represents a resource with attributes such as ID, name, year, color, and Pantone value.
    """

    def __init__(self, id: int, name: str, year: int, color: str, pantone_value: str):
        """
        Initializes a Resource object with the given attributes.

        Args:
            id (int): The ID of the resource.
            name (str): The name of the resource.
            year (int): The year associated with the resource.
            color (str): The color of the resource.
            pantone_value (str): The Pantone value of the resource.
        """
        self.id = id
        self.name = name
        self.year = year
        self.color = color
        self.pantone_value = pantone_value

    def fetch_resource(self, id: int, expected_status_code: int = 200) -> 'Resource':
        """
        Fetches a resource from the API.

        Args:
            id (int): The ID of the resource to fetch.
            expected_status_code (int): The expected HTTP status code.

        Returns:
            Resource: A Resource object retrieved from the API.

        Raises:
            AssertionError: If the response status code is not as expected.
            KeyError: If the expected "data" key is missing in the JSON response.
        """
        response = requests.get(f"{os.getenv('BASE_URL')}/unknown/{id}")
        assert response.status_code == expected_status_code, f"Unexpected status code: {response.status_code}"
        data = response.json()["data"]
        return Resource(**data)
