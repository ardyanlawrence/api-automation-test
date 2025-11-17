import os

import pytest
from faker import Faker
from client import ApiClient
from utility import ResponseValidator


class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_user_data(self, **overrides):
        base_data = {
            "name": self.fake.name(),
            "job": self.fake.job(),
            "email": self.fake.email(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name()
        }
        base_data.update(overrides)
        return base_data

    def generate_invalid_email(self):
        return self.fake.word()  # Email tanpa @

    def generate_long_string(self, length=1000):
        return 'a' * length


class TestReqResAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = ApiClient()
        self.validator = ResponseValidator()
        self.test_data = TestDataGenerator()
        print("\n" + "=" * 50)
        print("Setting up test environment")
        print("=" * 50)

    # Positive Test Cases
    def test_get_users_list(self):
        print("Testing GET /users - Positive Test")
        response = self.client.get("/users")
        data = response.json()
        self.validator.validate_status_code(response, 200)
        self.validator.validate_json_schema(response)
        self.validator.validate_response_contains(response, "data")
        self.validator.validate_response_time(response, 5)
        print(f"Response Data: {data}")
        assert len(data["data"]) > 0, "Should return at least one user"
        print("GET /users test passed")

    def test_create_user(self):
        print("Testing POST /users - Positive Test")
        user_data = self.test_data.generate_user_data()
        response = self.client.post("/users", json=user_data)
        data = response.json()
        self.validator.validate_status_code(response, 201)
        self.validator.validate_json_schema(response)
        self.validator.validate_response_contains(response, "name", user_data["name"])
        self.validator.validate_response_contains(response, "job", user_data["job"])
        self.validator.validate_response_contains(response, "id")
        print(f"Response Data: {data}")
        print("POST /users test passed")

    # ========== NEGATIVE TESTS ==========
    def test_get_nonexistent_user(self):
        print("Testing GET /users/999 - Negative Test")
        response = self.client.get("/users/999")
        self.validator.validate_status_code(response, 404)
        print("GET non-existent user test passed")

    # ========== BOUNDARY TESTS ==========
    def test_get_first_user(self):
        """Test mendapatkan user pertama - BOUNDARY"""
        print("Testing GET /users/1 - Boundary Test")
        response = self.client.get("/users/1")
        self.validator.validate_status_code(response, 200)
        self.validator.validate_json_schema(response)
        self.validator.validate_response_contains(response, "data")
        print("GET first user test passed")

    def test_get_last_user(self):
        """Test mendapatkan user terakhir - BOUNDARY"""
        print("Testing GET /users/12 - Boundary Test")
        response = self.client.get("/users/12")
        self.validator.validate_status_code(response, 200)
        self.validator.validate_json_schema(response)
        self.validator.validate_response_contains(response, "data")
        print("GET last user test passed")


# ==================== RUN TESTS ====================
if __name__ == "__main__":
    print("Starting API Automation Tests")
    print("=" * 60)
    print("Framework: Python with Requests and Pytest")
    print("API: ReqRes (https://reqres.in/)")
    print("Test Types: Positive, Negative, Boundary")
    print("=" * 60)
    report_dir = "reports"
    # os.makedirs(report_dir, exist_ok=True)
    exit_code = pytest.main([__file__, "-v", "--tb=short",
                             f"--html={report_dir}/test_report.html",
                             "--self-contained-html",
                             "--json-report",
                             f"--json-report-file={report_dir}/test_report.json",
                             "--json-report-indent=2"
                             ])
    print("=" * 60)
    if exit_code == 0:
        print("All tests passed successfully!")
    else:
        print("Some tests failed!")
    print("=" * 60)
