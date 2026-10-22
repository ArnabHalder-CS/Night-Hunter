# NIGHT HUNTER - Web Misconfiguration Checker

import requests

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


COMMON_FILES = [
    ".env",
    ".git/HEAD",
    "phpinfo.php",
    "server-status",
    "config.php",
    "backup.zip",
    "backup.sql"
]


def check_misconfiguration(url):

    findings = []

    try:
        log_info(f"Checking common misconfigurations: {url}")

        base_url = url.rstrip("/") + "/"

        for file_name in COMMON_FILES:

            target = base_url + file_name

            try:
                response = requests.get(
                    target,
                    timeout=DEFAULT_TIMEOUT,
                    allow_redirects=False
                )

                if response.status_code == 200:

                    findings.append(
                        Finding(
                            target=target,
                            category="Security Misconfiguration",
                            severity="High",
                            description=f"Potentially sensitive file or endpoint is accessible: {file_name}",
                            evidence=f"HTTP status code: {response.status_code}",
                            recommendation="Remove unnecessary sensitive files and restrict access to administrative or configuration resources."
                        )
                    )

                elif response.status_code in [401, 403]:

                    log_info(
                        f"Protected resource detected: {file_name} "
                        f"(HTTP {response.status_code})"
                    )

            except requests.RequestException:

                continue

        log_info("Misconfiguration check completed.")

    except Exception as error:

        log_error(f"Misconfiguration check failed: {error}")

    return findings