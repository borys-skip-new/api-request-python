import os
import requests
from typing import Optional
import requests
from utils.logger.logger import log_request, log_response


class Employee:
    """
    Represents an employee with attributes such as name, job, ID, and creation date.

    Attributes:
        name (str): The name of the employee.
        job (str): The job title of the employee.
        id (Optional[str]): The unique identifier of the employee. Defaults to None.
        created_at (Optional[str]): The creation timestamp of the employee. Defaults to None.
    """

    def __init__(self, name: str, job: str, id: Optional[str] = None, createdAt: Optional[str] = None):
        self.name = name
        self.job = job
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = ''

    def get_name(self) -> str:
        return self.name

    def get_job(self) -> str:
        return self.job

    def get_id(self) -> Optional[str]:
        return self.id

    def get_created_at(self) -> Optional[str]:
        return self.createdAt

    def get_updated_at(self) -> Optional[str]:
        return self.updatedAt
    
    def set_name(self, name: str) -> str:
        self.name = name
        return self

    def set_job(self, job: str) -> str:
        self.job = job
        return self
    
    def set_id(self, id: str) -> str:
        self.id = id
        return self
    
    def set_created_at(self, created_at: str):
        self.createdAt = created_at
        return self

    def set_updated_at(self, updated_at: str):
        self.updatedAt = updated_at
        return self  

    @staticmethod
    def create_employee_from_responce(employee_payload: 'EmployeeObject', expectedStatusCode: int = 201) -> 'Employee':
        """
        Sends a POST request to create a new employee.

        Args:
            employee_payload (EmployeeObject): The payload for creating the employee.
            expectedStatusCode (int): The expected HTTP status code.

        Returns:
            Employee: The created Employee object.
        """
        url = f"{os.getenv('BASE_URL')}/users"
        log_request("POST", url, employee_payload.__dict__)
        response = requests.post(url, json=employee_payload.__dict__)
        log_response(response)
        assert response.status_code == expectedStatusCode, f"Unexpected status code: {response.status_code}"
        response_data = response.json()
        return Employee(**response_data)

    def update_employee(self, expectedStatusCode: int = 200):
        """
        Sends a PUT request to update the employee's details.

        Args:
            expectedStatusCode (int): The expected HTTP status code.

        Returns:
            dict: The response data from the API.
        """
        url = f"{os.getenv('BASE_URL')}/users/{self.id}"
        log_request("PUT", url, self.__dict__)
        response = requests.put(url, json=self.__dict__)
        log_response(response)
        assert response.status_code == expectedStatusCode, f"Unexpected status code: {response.status_code}"
        self._update_employee_instance(response)

    def patch_employee(self, updates: dict, expectedStatusCode:int = 200):
        """
        Sends a PATCH request to partially update the employee's details.

        Args:
            base_url (str): The base URL of the API.
            updates (dict): A dictionary of fields to update.

        Returns:
            dict: The response data from the API.
        """
        url = f"{os.getenv('BASE_URL')}/users/{self.id}"
        log_request("PATCH", url, updates)
        response = requests.patch(url, json=updates)
        log_response(response)
        assert response.status_code == expectedStatusCode, f"Unexpected status code: {response.status_code}"
        self._update_employee_instance(response)


    def delete_employee(self, expectedStatusCode: int = 204):
        """
        Sends a DELETE request to remove the employee.

        Args:
            expectedStatusCode (int): The expected HTTP status code.

        Returns:
            int: 204 if the deletion was successful, or error code otherwise.
        """
        url = f"{os.getenv('BASE_URL')}/users/{self.id}"
        log_request("DELETE", url)
        response = requests.delete(url)
        log_response(response)
        assert response.status_code == expectedStatusCode
        return response.status_code
    

    def _update_employee_instance(self, response):
        """
        Updates the attributes of the Employee instance based on the API response.

        This method iterates through the keys and values in the JSON response
        and updates the corresponding attributes of the Employee instance if they exist.

        Args:
            response (requests.Response): The response object from the API containing updated employee data.
        """
        for key, value in response.json().items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        """
        Converts the Employee object into a dictionary.

        Returns:
            dict: A dictionary representation of the Employee object.
        """
        return self.__dict__

class EmployeeObject:
    """
    A class for creating Employee objects to be done via API request.

    This class provides a fluent interface for constructing Employee objects
    with optional attributes such as name, job.
    """
    def __init__(self):
        self.name = None
        self.job = None

    def set_name(self, name: str):
        self.name = name
        return self

    def set_job(self, job: str):
        self.job = job
        return self
