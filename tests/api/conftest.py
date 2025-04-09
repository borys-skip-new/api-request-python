import pytest
from dto.employee import Employee


"""
This module contains pytest fixtures for setting up test data for API tests.

Fixtures:
    employee_template (function): A class-scoped fixture that provides a template
    for creating employee objects during tests.
    employee (function): A class-scoped fixture that provides a dictionary
    for managing employee objects during tests.
"""

@pytest.fixture(scope="class")
def employee_template():
    """
    Provides a shared employee template instance for tests.

    This fixture initializes an employee template with predefined attributes.

    Yields:
        Employee: An instance of Employee used as a template.

    Scope:
        class (shared across all tests in a class)
    """
    yield Employee(name="morpheus", job="leader")
