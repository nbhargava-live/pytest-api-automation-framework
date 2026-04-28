# pytest-api-automation-framework

> Production-ready REST API test automation framework built with Python and pytest.  
> Designed for microservices architectures — covers authentication, response validation, schema checks, and CI/CD integration.

---

## About this project

This framework was built from hands-on experience testing distributed REST APIs at IBM (Watson Assistant, IBM Orchestrate) and enterprise SaaS platforms. It reflects real-world QA engineering patterns used in production environments with multiple release streams.

**Key capabilities:**
- Modular API client with session management and retry logic
- Schema validation using `jsonschema`
- Data-driven test execution via CSV/JSON fixtures
- Environment-based config management (dev / staging / prod)
- Allure HTML reporting with request/response logging
- GitHub Actions CI/CD pipeline (runs on every push and PR)

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Test runner | pytest |
| HTTP client | requests |
| Schema validation | jsonschema |
| Reporting | Allure |
| CI/CD | GitHub Actions |
| Config | python-dotenv |

---

## Project structure

```
pytest-api-automation-framework/
├── src/
│   ├── api_client/
│   │   ├── __init__.py
│   │   └── base_client.py        # Core HTTP client with retry & logging
│   ├── validators/
│   │   ├── __init__.py
│   │   └── response_validator.py # Schema + status + header validation
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py        # Load test data from JSON/CSV fixtures
├── tests/
│   ├── conftest.py               # Shared fixtures (auth, env config)
│   ├── test_auth.py              # Authentication flow tests
│   ├── test_users.py             # User API CRUD tests
│   └── test_schema_validation.py # Contract/schema tests
├── config/
│   ├── config.yaml               # Environment config
│   └── schemas/
│       └── user_schema.json      # JSON schema definitions
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions pipeline
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## Quick start

### 1. Clone and set up environment

```bash
git clone https://github.com/YOUR_USERNAME/pytest-api-automation-framework.git
cd pytest-api-automation-framework
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API base URL and credentials
```

### 3. Run tests

```bash
# Run all tests
pytest

# Run with Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Run a specific test file
pytest tests/test_users.py -v

# Run by marker (smoke, regression, auth)
pytest -m smoke -v
pytest -m regression -v
```

---

## CI/CD pipeline

Every push and pull request triggers the GitHub Actions workflow:

1. Spins up Python 3.10 environment
2. Installs dependencies
3. Runs the full test suite
4. Publishes Allure report as a build artifact

See `.github/workflows/ci.yml` for the full pipeline definition.

---

## Sample test output

```
tests/test_users.py::test_get_user_by_id PASSED
tests/test_users.py::test_create_user_returns_201 PASSED
tests/test_users.py::test_create_user_schema_valid PASSED
tests/test_users.py::test_unauthorized_returns_401 PASSED
tests/test_auth.py::test_login_with_valid_credentials PASSED
tests/test_auth.py::test_login_with_invalid_password PASSED
tests/test_schema_validation.py::test_user_response_schema PASSED

7 passed in 3.42s
```

---

## Author

**Nikita Bhargava** — Senior QA Engineer | SDET  
10+ years in quality engineering across IBM, Qualitest, and Tech Mahindra.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/nikita03-bhargava)
