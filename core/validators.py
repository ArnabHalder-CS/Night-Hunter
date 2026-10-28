"""
Input validation utilities for Night Hunter.
Prevents option injection, command-line tampering, and malicious payloads
from reaching underlying system calls, socket primitives, Nmap, or ping.
"""

import re
import ipaddress

_HOST_REGEX = re.compile(
    r"^(?=.{1,253}$)[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


def safe_host(raw: str) -> str:
    """
    Sanitize and validate a hostname or IP address.
    Strictly forbids option injection (e.g. -f, --script=...), spaces,
    and invalid characters.

    Returns the valid host string, or "" if invalid or hostile.
    """
    if not raw or not isinstance(raw, str):
        return ""

    h = raw.strip()

    # Strip scheme if present
    if "://" in h:
        h = h.split("://", 1)[1]

    # Strip paths, queries, fragments, credentials
    h = h.split("/")[0].split("?")[0].split("#")[0].rsplit("@", 1)[-1].strip()

    # Strip port if present (e.g. example.com:8080 or 1.1.1.1:443)
    if h.startswith("[") and "]" in h:
        inside = h[1:h.index("]")]
        try:
            ipaddress.IPv6Address(inside)
            return inside
        except ValueError:
            return ""
    elif h.count(":") == 1:
        h = h.split(":", 1)[0].strip()

    # Reject if empty, starts with dash (option injection), contains whitespace or shell metacharacters
    if not h or h.startswith("-") or any(c in h for c in " \t\r\n;|&`$><\\\"'"):
        return ""

    # Check if valid IP address (IPv4 or IPv6)
    try:
        ipaddress.ip_address(h)
        return h
    except ValueError:
        pass

    # Check if valid hostname / FQDN
    if _HOST_REGEX.match(h):
        return h

    return ""
