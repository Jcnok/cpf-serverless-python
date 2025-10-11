import json
import unittest.mock

import azure.functions as func
import pytest

# Import the function to be tested
from src.functions.cpf_validation.function_app import validate_cpf_handler

# --- Test Cases ---

def test_valid_cpf_returns_200(create_mock_request):
    """Test with a valid CPF number."""
    body = {"cpf": "11144477735"}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 200
    resp_body = json.loads(resp.get_body())
    assert resp_body["is_valid"] is True
    assert resp_body["message"] == "The provided CPF is valid."
    assert resp_body["cpf"] == body["cpf"]

def test_valid_formatted_cpf_returns_200(create_mock_request):
    """Test with a valid, formatted CPF number."""
    body = {"cpf": "111.444.777-35"}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 200
    resp_body = json.loads(resp.get_body())
    assert resp_body["is_valid"] is True
    assert resp_body["cpf"] == body["cpf"]

def test_valid_cpf_no_ip_header_returns_200(create_mock_request):
    """Test a valid CPF when X-Forwarded-For header is missing."""
    body = {"cpf": "11144477735"}
    # Pass an empty dictionary for headers to trigger the 'unknown' ip logic
    req = create_mock_request(body=body, headers={})
    resp = validate_cpf_handler(req)
    assert resp.status_code == 200
    resp_body = json.loads(resp.get_body())
    assert resp_body["is_valid"] is True

def test_invalid_cpf_returns_400(create_mock_request):
    """Test with an invalid CPF (wrong check digits)."""
    body = {"cpf": "11144477700"}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 400
    resp_body = json.loads(resp.get_body())
    assert resp_body["is_valid"] is False
    assert resp_body["message"] == "The provided CPF is invalid."
    assert resp_body["cpf"] == body["cpf"]

def test_repeated_digits_cpf_returns_400(create_mock_request):
    """Test with a CPF made of repeated digits."""
    body = {"cpf": "22222222222"}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 400
    resp_body = json.loads(resp.get_body())
    assert resp_body["is_valid"] is False
    assert resp_body["message"] == "The provided CPF is invalid."

def test_missing_cpf_field_returns_400(create_mock_request):
    """Test with a request body missing the 'cpf' field."""
    body = {"not_cpf": "12345"}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 400
    resp_body = json.loads(resp.get_body())
    assert resp_body["message"] == "Invalid request body. Ensure you provide a JSON with a \"cpf\" field."

def test_invalid_json_body_returns_400():
    """Test with a request body that is not valid JSON."""
    req = func.HttpRequest(
        method="POST",
        url="/api/validate-cpf",
        headers={'X-Forwarded-For': '127.0.0.1'},
        body=b'this is not json'
    )
    resp = validate_cpf_handler(req)
    assert resp.status_code == 400
    resp_body = json.loads(resp.get_body())
    assert resp_body["message"] == "Invalid JSON format in request body."

@unittest.mock.patch("src.functions.cpf_validation.function_app.is_rate_limited")
def test_rate_limit_exceeded_returns_429(mock_is_rate_limited, create_mock_request):
    """Test that a 429 is returned when the rate limit is exceeded."""
    mock_is_rate_limited.return_value = True
    body = {"cpf": "11144477735"}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 429
    resp_body = json.loads(resp.get_body())
    assert resp_body["message"] == "Too many requests. Please try again later."
    mock_is_rate_limited.assert_called_once_with('127.0.0.1')

@unittest.mock.patch("src.functions.cpf_validation.function_app.cpfcnpj.validate")
def test_generic_exception_returns_500(mock_validate, create_mock_request):
    """Test the generic exception handler returns a 500."""
    # Configure the mock to raise a generic exception
    mock_validate.side_effect = Exception("A wild error appeared!")

    body = {"cpf": "11144477735"}
    req = create_mock_request(body=body)

    # Call the function
    resp = validate_cpf_handler(req)

    # Assertions
    assert resp.status_code == 500
    resp_body = json.loads(resp.get_body())
    assert resp_body["message"] == "An internal server error occurred."

def test_cpf_field_not_a_string_returns_400(create_mock_request):
    """Test for a request where the 'cpf' field is not a string."""
    body = {"cpf": 12345678901}  # CPF as an integer
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 400
    resp_body = json.loads(resp.get_body())
    assert "Invalid request body" in resp_body["message"]

def test_empty_json_body_returns_400(create_mock_request):
    """Test for a request with an empty JSON object as the body."""
    body = {}
    req = create_mock_request(body=body)
    resp = validate_cpf_handler(req)
    assert resp.status_code == 400
    resp_body = json.loads(resp.get_body())
    assert "Invalid request body" in resp_body["message"]

@unittest.mock.patch("src.functions.cpf_validation.function_app.is_rate_limited")
def test_multiple_ips_in_header_uses_first_one(mock_is_rate_limited, create_mock_request):
    """Test that the first IP in X-Forwarded-For is used for rate limiting."""
    mock_is_rate_limited.return_value = False
    body = {"cpf": "11144477735"}
    headers = {"X-Forwarded-For": "192.168.1.1, 10.0.0.1"}
    req = create_mock_request(body=body, headers=headers)
    validate_cpf_handler(req)
    mock_is_rate_limited.assert_called_once_with("192.168.1.1")
