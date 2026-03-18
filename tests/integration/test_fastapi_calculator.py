# tests/integration/test_fastapi_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from fastapi.testclient import TestClient  # Import TestClient for simulating API requests
from main import app  # Import the FastAPI app instance from your main application file

# ---------------------------------------------
# Pytest Fixture: client
# ---------------------------------------------

@pytest.fixture
def client():
    """
    Pytest Fixture to create a TestClient for the FastAPI application.

    This fixture initializes a TestClient instance that can be used to simulate
    requests to the FastAPI application without running a live server. The client
    is yielded to the test functions and properly closed after the tests complete.

    Benefits:
    - Speeds up testing by avoiding the overhead of running a server.
    - Allows for testing API endpoints in isolation.
    """
    with TestClient(app) as client:
        yield client  # Provide the TestClient instance to the test functions

# ============================================
# SUCCESSFUL OPERATION TESTS
# ============================================

# Test Function: test_add_api

def test_add_api(client):
    """
    Test the Addition API Endpoint.

    This test verifies that the `/add` endpoint correctly adds two numbers provided
    in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/add` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`15`).
    """
    # Send a POST request to the '/add' endpoint with JSON payload
    response = client.post('/add', json={'a': 10, 'b': 5})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 15, f"Expected result 15, got {response.json()['result']}"

# Test Function: test_subtract_api

def test_subtract_api(client):
    """
    Test the Subtraction API Endpoint.

    This test verifies that the `/subtract` endpoint correctly subtracts the second number
    from the first number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/subtract` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/subtract' endpoint with JSON payload
    response = client.post('/subtract', json={'a': 10, 'b': 5})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# Test Function: test_multiply_api

def test_multiply_api(client):
    """
    Test the Multiplication API Endpoint.

    This test verifies that the `/multiply` endpoint correctly multiplies two numbers
    provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/multiply` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`50`).
    """
    # Send a POST request to the '/multiply' endpoint with JSON payload
    response = client.post('/multiply', json={'a': 10, 'b': 5})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 50, f"Expected result 50, got {response.json()['result']}"

# Test Function: test_divide_api

def test_divide_api(client):
    """
    Test the Division API Endpoint.

    This test verifies that the `/divide` endpoint correctly divides the first number
    by the second number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 2}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/divide' endpoint with JSON payload
    response = client.post('/divide', json={'a': 10, 'b': 2})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ============================================
# ERROR HANDLING TESTS
# ============================================

# Test Function: test_divide_by_zero_api

def test_divide_by_zero_api(client):
    """
    Test the Division by Zero API Endpoint.

    This test verifies that the `/divide` endpoint correctly handles division by zero
    by returning an appropriate error message and status code.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 0}`.
    2. Assert that the response status code is `400 Bad Request`.
    3. Assert that the JSON response contains an 'error' field with the message "Cannot divide by zero!".
    """
    # Send a POST request to the '/divide' endpoint with JSON payload attempting division by zero
    response = client.post('/divide', json={'a': 10, 'b': 0})

    # Assert that the response status code is 400
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Assert that the JSON response contains an 'error' field
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"

    # Assert that the 'error' field contains the correct error message
    assert "Cannot divide by zero!" in response.json()['error'], \
        f"Expected error message 'Cannot divide by zero!', got '{response.json()['error']}'"

# ============================================
# VALIDATION ERROR TESTS
# ============================================

@pytest.mark.parametrize(
    "endpoint, error_field",
    [
        ("/add", "a"),
        ("/add", "b"),
        ("/subtract", "a"),
        ("/subtract", "b"),
        ("/multiply", "a"),
        ("/multiply", "b"),
        ("/divide", "a"),
        ("/divide", "b"),
    ],
    ids=[
        "add_missing_a",
        "add_missing_b",
        "subtract_missing_a",
        "subtract_missing_b",
        "multiply_missing_a",
        "multiply_missing_b",
        "divide_missing_a",
        "divide_missing_b",
    ]
)
def test_missing_field_validation(client, endpoint, error_field):
    """
    Test validation error when required fields are missing.
    """
    # Create payload with missing field
    payload = {'a': 10, 'b': 5}
    payload.pop(error_field)

    # Send POST request with missing field
    response = client.post(endpoint, json=payload)

    # Assert 422 status code for validation error
    assert response.status_code == 422, f"Expected status 422, got {response.status_code} for {endpoint} missing {error_field}"

    # Assert error field is present
    assert 'error' in response.json(), f"Expected 'error' field in response for {endpoint}"


def test_invalid_content_type(client):
    """
    Test that invalid content type is handled correctly.
    """
    # Send POST request with plain text instead of JSON
    response = client.post(
        '/add',
        data='not json',
        headers={'Content-Type': 'text/plain'}
    )

    # Assert that validation fails with 422 status
    assert response.status_code == 422, f"Expected 422 for invalid content, got {response.status_code}"


def test_root_endpoint(client):
    """
    Test the root endpoint returns HTML response.
    """
    # Send GET request to root endpoint
    response = client.get('/')

    # Assert 200 status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Assert response contains HTML content
    assert 'text/html' in response.headers.get('content-type', ''), \
        f"Expected HTML content type, got {response.headers.get('content-type')}"

    # Assert response contains the heading
    assert 'Hello World' in response.text, "Expected 'Hello World' in response"

@pytest.mark.parametrize(
    "endpoint, a, b, expected",
    [
        ("/add",      -10, -5, -15.0),
        ("/subtract", -10, -5,  -5.0),
        ("/multiply", -10,  5, -50.0),
        ("/divide",   -10,  2,  -5.0),
    ],
    ids=["add_negatives", "subtract_negatives", "multiply_negatives", "divide_negatives"],
)
def test_negative_numbers(client, endpoint, a, b, expected):
    """Test that all endpoints handle negative number inputs correctly."""
    response = client.post(endpoint, json={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json()["result"] == expected


@pytest.mark.parametrize(
    "endpoint",
    ["/add", "/subtract", "/multiply", "/divide"],
    ids=["add_string", "subtract_string", "multiply_string", "divide_string"],
)
def test_string_input_returns_error(client, endpoint):
    """Test that sending string values for a or b returns a validation error."""
    response = client.post(endpoint, json={"a": "foo", "b": 5})
    assert response.status_code in (400, 422), (
        f"Expected 400 or 422, got {response.status_code}"
    )
    assert "error" in response.json() or "detail" in response.json()

@pytest.mark.parametrize(
    "endpoint, a, b, expected",
    [
        ("/add",      2.5,  3.5,  6.0),
        ("/subtract", 5.5,  2.5,  3.0),
        ("/multiply", 2.5,  4.0, 10.0),
        ("/divide",   7.5,  2.5,  3.0),
    ],
    ids=["add_floats", "subtract_floats", "multiply_floats", "divide_floats"],
)
def test_floats(client, endpoint, a, b, expected):
    """Endpoints handle floating-point numbers"""
    response = client.post(endpoint, json={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json()["result"] == expected
