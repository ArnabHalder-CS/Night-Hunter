# NIGHT HUNTER - Injection Security Checker

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


SQL_TEST_VALUES = [
    "'",
    '"',
    "1'",
    "1\""
]


SQL_ERROR_PATTERNS = [
    "sql syntax",
    "mysql",
    "mysqli",
    "postgresql",
    "sqlite",
    "ora-",
    "odbc",
    "jdbc",
    "syntax error",
    "unclosed quotation mark"
]


def check_sql_injection(url):

    findings = []

    try:
        parsed_url = urlparse(url)

        parameters = parse_qs(parsed_url.query)

        if not parameters:
            log_info("No URL parameters found for SQL injection testing.")
            return findings

        log_info(f"Testing URL parameters for SQL injection indicators: {url}")

        for parameter in parameters:

            original_value = parameters[parameter][0]

            for test_value in SQL_TEST_VALUES:

                modified_parameters = parameters.copy()
                modified_parameters[parameter] = [
                    original_value + test_value
                ]

                modified_query = urlencode(
                    modified_parameters,
                    doseq=True
                )

                test_url = urlunparse((
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    modified_query,
                    parsed_url.fragment
                ))

                try:
                    response = requests.get(
                        test_url,
                        timeout=DEFAULT_TIMEOUT,
                        allow_redirects=True
                    )

                    response_text = response.text.lower()

                    for error_pattern in SQL_ERROR_PATTERNS:

                        if error_pattern in response_text:

                            findings.append(
                                Finding(
                                    target=url,
                                    category="Injection",
                                    severity="High",
                                    description=(
                                        f"Possible SQL injection indicator "
                                        f"found in parameter: {parameter}"
                                    ),
                                    evidence=(
                                        f"Database-related error pattern "
                                        f"detected: {error_pattern}"
                                    ),
                                    recommendation=(
                                        "Use parameterized queries or "
                                        "prepared statements and validate "
                                        "user input."
                                    )
                                )
                            )

                            break

                except requests.RequestException:

                    continue

        log_info("SQL injection indicator check completed.")

    except Exception as error:

        log_error(f"SQL injection check failed: {error}")

    return findings