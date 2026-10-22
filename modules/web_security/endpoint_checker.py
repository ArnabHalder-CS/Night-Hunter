# NIGHT HUNTER - Endpoint Checker

import requests
from urllib.parse import urljoin

from core.config import DEFAULT_TIMEOUT
from core.logger import log_info, log_error


COMMON_ENDPOINTS = [
    "robots.txt",
    "sitemap.xml",
    ".well-known/security.txt",
    "login",
    "admin",
]


def check_endpoints(url):

    results = []

    try:
        log_info(f"Checking common endpoints: {url}")

        base_url = url.rstrip("/") + "/"

        for endpoint in COMMON_ENDPOINTS:

            target = urljoin(base_url, endpoint)

            try:
                response = requests.get(
                    target,
                    timeout=DEFAULT_TIMEOUT,
                    allow_redirects=True
                )

                result = {
                    "endpoint": endpoint,
                    "url": target,
                    "status_code": response.status_code,
                    "found": response.status_code < 400
                }

                results.append(result)

            except requests.RequestException:

                results.append({
                    "endpoint": endpoint,
                    "url": target,
                    "status_code": None,
                    "found": False
                })

        log_info("Endpoint check completed.")

        return results

    except Exception as error:

        log_error(f"Endpoint check failed: {error}")

        return []