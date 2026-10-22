# NIGHT HUNTER - Cookie Security Checker

import requests

from core.config import DEFAULT_TIMEOUT
from core.finding import Finding
from core.logger import log_info, log_error


def scan_cookies(url):

    findings = []

    try:
        log_info(f"Checking cookie security: {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True
        )

        cookies = response.cookies

        if not cookies:
            log_info("No cookies were set by the response.")
            return findings

        for cookie in cookies:

            cookie_name = cookie.name

            secure = cookie.secure

            http_only = cookie.has_nonstandard_attr("HttpOnly")

            same_site = cookie.get_nonstandard_attr("SameSite")

            if not secure:

                findings.append(
                    Finding(
                        target=url,
                        category="Cookie Security",
                        severity="Medium",
                        description=f"Cookie '{cookie_name}' does not have the Secure flag.",
                        evidence=f"Cookie '{cookie_name}' was received without the Secure attribute.",
                        recommendation="Use the Secure attribute for cookies that should only be sent over HTTPS."
                    )
                )

            if not http_only:

                findings.append(
                    Finding(
                        target=url,
                        category="Cookie Security",
                        severity="Medium",
                        description=f"Cookie '{cookie_name}' does not have the HttpOnly flag.",
                        evidence=f"Cookie '{cookie_name}' was received without the HttpOnly attribute.",
                        recommendation="Use HttpOnly for cookies that do not need to be accessed by client-side JavaScript."
                    )
                )

            if not same_site:

                findings.append(
                    Finding(
                        target=url,
                        category="Cookie Security",
                        severity="Low",
                        description=f"Cookie '{cookie_name}' does not specify a SameSite attribute.",
                        evidence=f"Cookie '{cookie_name}' has no SameSite attribute in the response.",
                        recommendation="Configure an appropriate SameSite policy based on the application's requirements."
                    )
                )

        log_info("Cookie security check completed.")

    except requests.RequestException as error:

        log_error(f"Cookie check failed: {error}")

    return findings