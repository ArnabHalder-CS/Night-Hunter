# NIGHT HUNTER - Session Security Checker

import requests

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


def check_session(url):

    findings = []

    try:
        log_info(f"Checking session security indicators: {url}")

        session = requests.Session()

        response = session.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True
        )

        cookies = response.cookies

        if cookies:

            for cookie in cookies:

                cookie_name = cookie.name

                if not cookie.secure:

                    findings.append(
                        Finding(
                            target=url,
                            category="Session Security",
                            severity="Medium",
                            description=(
                                f"Session-related cookie '{cookie_name}' "
                                "does not use the Secure flag."
                            ),
                            evidence=(
                                f"Cookie '{cookie_name}' was received "
                                "without the Secure attribute."
                            ),
                            recommendation=(
                                "Use the Secure attribute for sensitive "
                                "session cookies."
                            )
                        )
                    )

                if not cookie.has_nonstandard_attr("HttpOnly"):

                    findings.append(
                        Finding(
                            target=url,
                            category="Session Security",
                            severity="Medium",
                            description=(
                                f"Cookie '{cookie_name}' does not use "
                                "the HttpOnly flag."
                            ),
                            evidence=(
                                f"Cookie '{cookie_name}' was received "
                                "without the HttpOnly attribute."
                            ),
                            recommendation=(
                                "Use HttpOnly for sensitive session "
                                "cookies when client-side access is not required."
                            )
                        )
                    )

        else:

            log_info("No cookies were set by the response.")

        log_info("Session security check completed.")

    except requests.RequestException as error:

        log_error(
            f"Session security check failed: {error}"
        )

    return findings