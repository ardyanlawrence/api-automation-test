import json

import pytest


class ResponseValidator:
    @staticmethod
    def validate_status_code(response, expected_code):
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, but got {response.status_code}"

    @staticmethod
    def validate_json_schema(response):
        try:
            response.json()
            return True
        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")

    @staticmethod
    def validate_response_time(response, max_time=3):
        assert response.elapsed.total_seconds() < max_time, \
            f"Response time {response.elapsed.total_seconds():.2f}s exceeded {max_time} seconds"

    @staticmethod
    def validate_response_contains(response, key, value=None):
        response_json = response.json()
        assert key in response_json, f"Key '{key}' not found in response"

        if value is not None:
            assert response_json[key] == value, \
                f"Expected '{key}' to be '{value}', but got '{response_json[key]}'"
        return True

    @staticmethod
    def validate_empty_data_array(response):
        response_json = response.json()
        assert "data" in response_json, "Response should contain 'data' key"
        assert isinstance(response_json["data"], list), "Data should be a list"
        assert len(response_json["data"]) == 0, "Data array should be empty"
        return True