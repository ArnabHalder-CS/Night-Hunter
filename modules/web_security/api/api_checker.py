# NIGHT HUNTER - API Security Checker

import requests
from urllib.parse import urljoin

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


COMMON_API_PATHS = [
    "api/",
    "api/v1/",
    "api/v2/",
    "swagger/",
    "swagger-ui/",
    "openapi.json",
    "api-docs/"
]


def check_api_exposure(url):

    findings = []

    try:
        log_info(f"Checking common API endpoints: {url}")

        base_url = url.rstrip("/") + "/"

        for path in COMMON_API_PATHS:

            target = urljoin(base_url, path)

            try:
                response = requests.get(
                    target,
                    timeout=DEFAULT_TIMEOUT,
                    allow_redirects=False
                )

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                ).lower()

                if response.status_code == 200:

                    findings.append(
                        Finding(
                            target=target,
                            category="API Security",
                            severity="Info",
                            description=f"Potential API or API documentation endpoint found: {path}",
                            evidence=(
                                f"HTTP status: {response.status_code}, "
                                f"Content-Type: {content_type}"
                            ),
                            recommendation=(
                                "Review whether this endpoint should be "
                                "publicly accessible and ensure proper "
                                "authentication and authorization."
                            )
                        )
                    )

            except requests.RequestException:

                continue

        log_info("API exposure check completed.")

    except Exception as error:

        log_error(f"API security check failed: {error}")

    return findings