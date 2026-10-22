# NIGHT HUNTER - Technology Detector

import re
import requests

from core.config import DEFAULT_TIMEOUT
from core.logger import log_info, log_error


def detect_technologies(url):

    technologies = []

    try:
        log_info(f"Detecting web technologies: {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True
        )

        headers = response.headers
        body = response.text

        # Web server
        server = headers.get("Server")

        if server:
            technologies.append({
                "type": "Web Server",
                "name": server,
                "source": "Server header"
            })

        # Powered-by information
        powered_by = headers.get("X-Powered-By")

        if powered_by:
            technologies.append({
                "type": "Technology",
                "name": powered_by,
                "source": "X-Powered-By header"
            })

        # WordPress
        if "wp-content" in body or "wp-includes" in body:

            technologies.append({
                "type": "CMS",
                "name": "WordPress",
                "source": "HTML content"
            })

        # React
        if (
            "react" in body.lower()
            or "reactroot" in body.lower()
        ):

            technologies.append({
                "type": "JavaScript Framework",
                "name": "React",
                "source": "HTML content"
            })

        # Vue
        if "vue" in body.lower():

            technologies.append({
                "type": "JavaScript Framework",
                "name": "Vue.js",
                "source": "HTML content"
            })

        # Angular
        if (
            "ng-version" in body.lower()
            or re.search(r"angular", body, re.IGNORECASE)
        ):

            technologies.append({
                "type": "JavaScript Framework",
                "name": "Angular",
                "source": "HTML content"
            })

        # jQuery
        if re.search(r"jquery[\.-]?\d", body, re.IGNORECASE):

            technologies.append({
                "type": "JavaScript Library",
                "name": "jQuery",
                "source": "HTML content"
            })

        log_info("Technology detection completed.")

        return technologies

    except requests.RequestException as error:

        log_error(f"Technology detection failed: {error}")

        return []