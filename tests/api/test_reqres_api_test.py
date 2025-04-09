import pytest
from dto.employee import Employee, EmployeeObject
from dto.user_class import User
from dto.resource_class import Resource
import json
from utils.logger.logger import log

class TestUser:
    def setup_method(self):
        self.user = User()

    @pytest.mark.step("Fetch users and validate response")
    def test_get_users(self):
        users = self.user.fetch_users()
        assert len(users) == 6
        assert isinstance(users[0], User)

class TestEmployee:
    actual_employee = None

    @pytest.mark.step("Create an employee and validate response")
    def test_create_employee(self, employee_template, caplog):
        with caplog.at_level("INFO"):
            log.info("Starting test_create_employee")
            
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
        assert "Starting test_create_employee" in caplog.text

    @pytest.mark.parametrize("new_position", ["test engineer", "matrix operator", "oracle assistant"])
    @pytest.mark.step("Update an employee's job and validate response")
    def test_update_employee(self, employee_template, new_position):
        TestEmployee.actual_employee.set_name(employee_template.get_name()).set_job(new_position).update_employee()
        assert TestEmployee.actual_employee.get_name() == employee_template.get_name()
        assert TestEmployee.actual_employee.get_job() == new_position
        assert TestEmployee.actual_employee.get_updated_at() is not None

    @pytest.mark.step("Patch an employee's details and validate response")
    def test_patch_employee(self):
        updated_name = "Updated Name"
        updated_job = "Updated Job"
        TestEmployee.actual_employee.patch_employee({"name": "Updated Name", "job": "Updated Job"})
        assert TestEmployee.actual_employee.get_name() == updated_name
        assert TestEmployee.actual_employee.get_job() == updated_job
        assert TestEmployee.actual_employee.get_updated_at() is not None

    @pytest.mark.step("Delete an employee and validate response")
    def test_delete_employeer(self):
        result = TestEmployee.actual_employee.delete_employee()
        assert result == 204

class TestResource:
    @pytest.mark.parametrize("expected_value", json.load(open("test_data/expected_resource.json")))
    @pytest.mark.step("Fetch a resource and validate response")
    def test_get_resource(self, expected_value):
        template = Resource(**expected_value)
        resource = template.fetch_resource(expected_value["id"])
        assert resource.id == expected_value["id"]
        assert resource.name == expected_value["name"]
        assert resource.year == expected_value["year"]
        assert resource.color == expected_value["color"]
        assert resource.pantone_value == expected_value["pantone_value"]
