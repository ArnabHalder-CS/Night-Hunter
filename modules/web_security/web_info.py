# NIGHT HUNTER - Web Information

import requests
from urllib.parse import urlparse

from core.config import DEFAULT_TIMEOUT
from core.logger import log_info, log_error


def get_web_info(url):

    try:
        log_info(f"Gathering web information: {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True
        )

        parsed_url = urlparse(response.url)

        info = {
            "original_url": url,
            "final_url": response.url,
            "scheme": parsed_url.scheme,
            "hostname": parsed_url.hostname,
            "status_code": response.status_code,
            "server": response.headers.get("Server", "Not disclosed"),
            "content_type": response.headers.get(
                "Content-Type",
                "Not disclosed"
            ),
            "content_length": response.headers.get(
                "Content-Length",
                "Not disclosed"
            )
        }

        log_info("Web information collected.")

        return info

    except requests.RequestException as error:

        log_error(f"Unable to collect web information: {error}")

        return None