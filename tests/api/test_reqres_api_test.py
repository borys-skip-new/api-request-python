import pytest
from dto.employee import Employee, EmployeeObject
from dto.user_class import User
from dto.resource_class import Resource
import json
from tests.api.base_test import BaseTest
from utils.logger.logger import log

class TestUser(BaseTest):
    def setup_method(self):
        self.user = User()
        self.test_name = self.__class__.__name__

    @pytest.mark.step("Fetch users and validate response")
    def test_get_users(self):
        
        log.info(f"Starting {self.test_name}")
        users = self.user.fetch_users()
        assert len(users) == 6
        assert isinstance(users[0], User)

class TestEmployee(BaseTest):
    def setup_method(self, method, request):
        """
        Setup method to initialize the test name from the @pytest.mark.step decorator.
        """
        marker = request.node.get_closest_marker("step")
        self.test_name = marker.args[0] if marker and marker.args else method.__name__

    actual_employee = None

    @pytest.mark.step("Create an employee and validate response")
    def test_create_employee(self, employee_template):
        log.info(f"Starting {self.test_name}")
            
        TestEmployee.actual_employee = Employee.create_employee_from_responce(
            EmployeeObject()
            .set_name(employee_template.get_name())
            .set_job(employee_template.get_job())
        )
        log.info(f"Created employee: {json.dumps(TestEmployee.actual_employee.to_dict())}")
        assert TestEmployee.actual_employee.get_name() == employee_template.get_name()
        assert TestEmployee.actual_employee.get_job() == employee_template.get_job()
        assert TestEmployee.actual_employee.get_created_at() is not None
        assert TestEmployee.actual_employee.id is not None

    @pytest.mark.parametrize("new_position", ["test engineer", "matrix operator", "oracle assistant"])
    @pytest.mark.step("Update an employee's job and validate response")
    def test_update_employee(self, employee_template, new_position):
        log.info(f"Starting {self.test_name}")
        TestEmployee.actual_employee.set_name(employee_template.get_name()).set_job(new_position).update_employee()
        assert TestEmployee.actual_employee.get_name() == employee_template.get_name()
        assert TestEmployee.actual_employee.get_job() == new_position
        assert TestEmployee.actual_employee.get_updated_at() is not None

    @pytest.mark.step("Patch an employee's details and validate response")
    def test_patch_employee(self):
        updated_name = "Updated Name"
        updated_job = "Updated Job"
        log.info(f"Starting {self.test_name}")
        TestEmployee.actual_employee.patch_employee({"name": "Updated Name", "job": "Updated Job"})
        assert TestEmployee.actual_employee.get_name() == updated_name
        assert TestEmployee.actual_employee.get_job() == updated_job
        assert TestEmployee.actual_employee.get_updated_at() is not None

    @pytest.mark.step("Delete an employee and validate response")
    def test_delete_employeer(self):
        log.info(f"Starting {self.test_name}")
        result = TestEmployee.actual_employee.delete_employee()
        assert result == 204

class TestResource(BaseTest):
    def setup_method(self):
        self.test_name = self.__class__.__name__

    @pytest.mark.parametrize("expected_value", json.load(open("test_data/expected_resource.json")))
    @pytest.mark.step("Fetch a resource and validate response")
    def test_get_resource(self, expected_value):
        log.info(f"Starting {self.test_name}")
        template = Resource(**expected_value)
        resource = template.fetch_resource(expected_value["id"])
        assert resource.id == expected_value["id"]
        assert resource.name == expected_value["name"]
        assert resource.year == expected_value["year"]
        assert resource.color == expected_value["color"]
        assert resource.pantone_value == expected_value["pantone_value"]
