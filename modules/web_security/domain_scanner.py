# ============================================================
# NIGHT HUNTER - Domain & Web Intelligence Scanner
# ============================================================
# Normal web scanner providing domain intelligence, DNS, SSL/TLS,
# server technology, and defensive security headers without aggressive exploits.

import socket
import ssl
import time
import urllib.parse
from datetime import datetime
import requests

from core.logger import log_info, log_error

DEFAULT_TIMEOUT = 5.0

STANDARD_SECURITY_HEADERS = {
    "Strict-Transport-Security": "Enforces HTTPS connections and prevents SSL stripping.",
    "Content-Security-Policy": "Restricts sources of executable scripts, stylesheets, and images.",
    "X-Frame-Options": "Protects users against clickjacking attacks.",
    "X-Content-Type-Options": "Prevents MIME-type sniffing of uploaded files.",
    "Referrer-Policy": "Controls how much referrer information is included with requests.",
    "Permissions-Policy": "Restricts browser features like camera, microphone, and geolocation."
}


def analyze_domain(url: str) -> dict:
    """Analyze domain and web server parameters cleanly and safely."""
    raw_target = url.strip()
    if not raw_target.startswith(("http://", "https://")):
        target_url = "https://" + raw_target
    else:
        target_url = raw_target

    parsed = urllib.parse.urlparse(target_url)
    hostname = parsed.hostname or raw_target
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    report = {
        "target": target_url,
        "recon": {
            "hostname": hostname,
            "domain": hostname,
            "ip_address": "",
            "addresses": [],
            "status_code": None,
            "status_text": "",
            "server": "Unknown",
            "final_url": target_url,
            "scheme": parsed.scheme,
            "content_type": "",
            "content_length": "",
            "latency_ms": 0,
        },
        "tls": {
            "has_tls": False,
            "tls_version": "N/A",
            "cipher": "N/A",
            "issuer": "N/A",
            "certificate_expiry": "N/A",
            "days_remaining": None,
            "valid": False,
        },
        "dns": {
            "ipv4": [],
            "canonical_name": "",
        },
        "security_headers": [],
        "technology": [],
        "cookies": [],
        "endpoints": [],
        "ports": [],
        "report_summary": {
            "total": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
    }

    # 1. DNS Resolution
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        ips = sorted(list(set(item[4][0] for item in addr_info if item[4])))
        report["dns"]["ipv4"] = ips
        report["recon"]["addresses"] = ips
        if ips:
            report["recon"]["ip_address"] = ips[0]
    except Exception as dns_err:
        log_error(f"DNS resolution failed for {hostname}: {dns_err}")

    # 2. HTTP Request & Latency
    t0 = time.time()
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        response = requests.get(target_url, timeout=DEFAULT_TIMEOUT, headers=headers, allow_redirects=True)
        elapsed_ms = int((time.time() - t0) * 1000)

        report["recon"]["status_code"] = response.status_code
        report["recon"]["status_text"] = response.reason or "OK"
        report["recon"]["final_url"] = response.url
        report["recon"]["server"] = response.headers.get("Server", "Undisclosed")
        report["recon"]["content_type"] = response.headers.get("Content-Type", "")
        report["recon"]["latency_ms"] = elapsed_ms

        content_len = response.headers.get("Content-Length")
        if content_len:
            try:
                report["recon"]["content_length"] = f"{round(int(content_len) / 1024, 1)} KB"
            except Exception:
                report["recon"]["content_length"] = f"{content_len} B"
        elif response.content:
            report["recon"]["content_length"] = f"{round(len(response.content) / 1024, 1)} KB"

        # Security Headers Evaluation
        for header, description in STANDARD_SECURITY_HEADERS.items():
            present = header.lower() in [h.lower() for h in response.headers.keys()]
            val = next((v for k, v in response.headers.items() if k.lower() == header.lower()), None)
            report["security_headers"].append({
                "header": header,
                "present": present,
                "value": val or "Missing",
                "recommendation": description
            })
            if not present:
                report["report_summary"]["medium"] += 1
                report["report_summary"]["total"] += 1

        # Technology Detection from headers
        detected_tech = []
        if "cloudflare" in response.headers.get("Server", "").lower() or "cf-ray" in response.headers:
            detected_tech.append({"name": "Cloudflare CDN / Proxy", "category": "CDN / Security"})
        if "nginx" in response.headers.get("Server", "").lower():
            detected_tech.append({"name": "Nginx Web Server", "category": "Web Server"})
        elif "apache" in response.headers.get("Server", "").lower():
            detected_tech.append({"name": "Apache HTTP Server", "category": "Web Server"})
        elif "litespeed" in response.headers.get("Server", "").lower():
            detected_tech.append({"name": "LiteSpeed Web Server", "category": "Web Server"})
        elif "gunicorn" in response.headers.get("Server", "").lower() or "waitress" in response.headers.get("Server", "").lower():
            detected_tech.append({"name": "Python WSGI Server", "category": "Application Server"})

        x_powered = response.headers.get("X-Powered-By")
        if x_powered:
            detected_tech.append({"name": x_powered, "category": "Framework / Engine"})

        report["technology"] = detected_tech

        # Cookie Inspection
        cookie_list = []
        for c in response.cookies:
            cookie_list.append({
                "name": c.name,
                "domain": c.domain,
                "path": c.path,
                "secure": c.secure,
                "httponly": bool(c.has_nonstandard_attr("HttpOnly"))
            })
        report["cookies"] = cookie_list

    except Exception as req_err:
        log_error(f"HTTP request failed for {target_url}: {req_err}")
        report["recon"]["status_text"] = "Connection Failed"

    # 3. SSL/TLS Certificate Analysis
    ssl_port = port if (port and port != 80) else 443
    if target_url.startswith("https://") or ssl_port == 443 or port == 8443:
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((hostname, ssl_port), timeout=3.0) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    tls_ver = ssock.version()
                    issuer_dict = dict(x[0] for x in cert.get("issuer", []))
                    not_after = cert.get("notAfter")

                    days_left = None
                    if not_after:
                        try:
                            # Format: 'Dec 21 18:38:32 2026 GMT'
                            exp_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                            days_left = (exp_date - datetime.utcnow()).days
                        except Exception:
                            pass

                    is_expiring = days_left is not None and days_left < 15
                    if is_expiring:
                        report["report_summary"]["high"] += 1
                        report["report_summary"]["total"] += 1

                    report["tls"] = {
                        "has_tls": True,
                        "tls_version": tls_ver or "TLSv1.3",
                        "cipher": cipher[0] if cipher else "Strong Cipher",
                        "issuer": issuer_dict.get("commonName") or issuer_dict.get("organizationName", "Verified CA"),
                        "certificate_expiry": not_after or "Valid",
                        "days_remaining": days_left,
                        "valid": True
                    }
        except (socket.timeout, TimeoutError):
            log_error(f"SSL handshake timeout for {hostname}:{ssl_port}")
            report["tls"]["tls_version"] = "Connection Timeout"
            report["tls"]["valid"] = False
            report["report_summary"]["low"] += 1
            report["report_summary"]["total"] += 1
        except ssl.SSLCertVerificationError as ssl_err:
            log_error(f"SSL certificate verification failed for {hostname}: {ssl_err}")
            report["tls"]["tls_version"] = "Invalid / Self-Signed Certificate"
            report["tls"]["valid"] = False
            report["report_summary"]["high"] += 1
            report["report_summary"]["total"] += 1
        except Exception as ssl_err:
            log_error(f"SSL handshake error for {hostname}: {ssl_err}")
            report["tls"]["tls_version"] = f"SSL Error ({type(ssl_err).__name__})"
            report["tls"]["valid"] = False
            report["report_summary"]["medium"] += 1
            report["report_summary"]["total"] += 1
    elif not target_url.startswith("https://"):
        # Plaintext unencrypted HTTP
        report["report_summary"]["high"] += 1
        report["report_summary"]["total"] += 1

    return report
