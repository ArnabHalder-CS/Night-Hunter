# NIGHT HUNTER - Authentication Security Checker

import requests

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


def check_authentication(url):

    findings = []

    try:
        log_info(f"Checking authentication security indicators: {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True
        )

        body = response.text.lower()

        login_indicators = [
            "login",
            "sign in",
            "signin",
            "username",
            "password"
        ]

        detected = []

        for indicator in login_indicators:

            if indicator in body:
                detected.append(indicator)

        if detected:

            log_info(
                "Authentication-related page indicators detected."
            )

        else:

            log_info(
                "No obvious authentication indicators detected."
            )

        # Check whether HTTPS is being used
        if response.url.lower().startswith("http://"):

            findings.append(
                Finding(
                    target=url,
                    category="Authentication",
                    severity="High",
                    description="Authentication-related page is being accessed over HTTP.",
                    evidence=f"Final URL: {response.url}",
                    recommendation=(
                        "Use HTTPS for authentication pages so credentials "
                        "and authentication data are protected in transit."
                    )
                )
            )

        # Check common authentication response headers
        if "Cache-Control" not in response.headers:

            findings.append(
                Finding(
                    target=url,
                    category="Authentication",
                    severity="Low",
                    description="Cache-Control header was not detected.",
                    evidence="No Cache-Control header in the response.",
                    recommendation=(
                        "Review caching rules for authentication-related "
                        "pages and sensitive responses."
                    )
                )
            )

        log_info("Authentication security check completed.")

    except requests.RequestException as error:

        log_error(
            f"Authentication check failed: {error}"
        )

    return findings