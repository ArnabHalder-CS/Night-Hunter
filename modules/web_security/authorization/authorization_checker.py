# NIGHT HUNTER - Authorization Security Checker

import requests
from urllib.parse import urljoin

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


COMMON_PROTECTED_PATHS = [
    "admin/",
    "dashboard/",
    "account/",
    "profile/",
    "manage/",
    "settings/"
]


def check_authorization(url):

    findings = []

    try:
        log_info(f"Checking access-control indicators: {url}")

        base_url = url.rstrip("/") + "/"

        for path in COMMON_PROTECTED_PATHS:

            target = urljoin(base_url, path)

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
                            category="Authorization",
                            severity="Medium",
                            description=(
                                f"Potentially protected resource is "
                                f"accessible without an authentication "
                                f"session: {path}"
                            ),
                            evidence=(
                                f"HTTP status code: "
                                f"{response.status_code}"
                            ),
                            recommendation=(
                                "Verify that server-side authorization "
                                "checks are enforced before allowing "
                                "access to protected resources."
                            )
                        )
                    )

                elif response.status_code in [401, 403]:

                    log_info(
                        f"Access control response detected for {path}: "
                        f"HTTP {response.status_code}"
                    )

            except requests.RequestException:
                continue

        log_info("Authorization check completed.")

    except Exception as error:

        log_error(
            f"Authorization check failed: {error}"
        )

    return findings