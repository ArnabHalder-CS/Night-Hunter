# NIGHT HUNTER - Security Headers Scanner

import requests

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "severity": "Medium",
        "description": "Content Security Policy header is missing.",
        "recommendation": "Configure a suitable Content-Security-Policy."
    },

    "Strict-Transport-Security": {
        "severity": "Medium",
        "description": "Strict-Transport-Security header is missing.",
        "recommendation": "Enable HSTS when the website is correctly configured for HTTPS."
    },

    "X-Content-Type-Options": {
        "severity": "Low",
        "description": "X-Content-Type-Options header is missing.",
        "recommendation": "Set X-Content-Type-Options to nosniff."
    },

    "X-Frame-Options": {
        "severity": "Medium",
        "description": "X-Frame-Options header is missing.",
        "recommendation": "Use an appropriate clickjacking protection policy."
    },

    "Referrer-Policy": {
        "severity": "Low",
        "description": "Referrer-Policy header is missing.",
        "recommendation": "Configure a suitable Referrer-Policy."
    },

    "Permissions-Policy": {
        "severity": "Low",
        "description": "Permissions-Policy header is missing.",
        "recommendation": "Configure Permissions-Policy according to the application's requirements."
    }
}


def scan_security_headers(url):

    findings = []

    try:
        log_info(f"Scanning security headers: {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True
        )

        headers = response.headers

        for header, details in SECURITY_HEADERS.items():

            if header not in headers:

                finding = Finding(
                    target=url,
                    category="Security Headers",
                    severity=details["severity"],
                    description=details["description"],
                    evidence=f"{header} was not present in the HTTP response.",
                    recommendation=details["recommendation"]
                )

                findings.append(finding)

        log_info("Security header scan completed.")

        return findings

    except requests.RequestException as error:

        log_error(f"Security header scan failed: {error}")

        return []