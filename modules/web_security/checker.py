# NIGHT HUNTER - Web Security Checker

import requests

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


def check_security_headers(url):

    findings = []

    try:
        log_info(f"Checking security headers: {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT
        )

        headers = response.headers

        security_headers = {
            "Content-Security-Policy": "Helps control which resources a website can load.",
            "X-Frame-Options": "Helps protect against clickjacking.",
            "X-Content-Type-Options": "Helps prevent MIME-type sniffing.",
            "Strict-Transport-Security": "Helps enforce HTTPS connections.",
            "Referrer-Policy": "Controls referrer information sent by the browser."
        }

        for header, description in security_headers.items():

            if header not in headers:

                finding = Finding(
                    target=url,
                    category="Security Headers",
                    severity="Medium",
                    description=f"Missing security header: {header}",
                    evidence=f"{header} was not found in the HTTP response.",
                    recommendation=description
                )

                findings.append(finding)

        log_info("Security header check completed.")

    except requests.RequestException as error:

        log_error(f"Request failed: {error}")

    return findings