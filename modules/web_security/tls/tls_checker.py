# NIGHT HUNTER - TLS / HTTPS Checker

import socket
import ssl
from datetime import datetime
from urllib.parse import urlparse

from core.finding import Finding
from core.logger import log_info, log_error


def scan_tls(url):

    findings = []

    try:
        parsed_url = urlparse(url)

        hostname = parsed_url.hostname
        port = parsed_url.port or 443

        if not hostname:
            log_error("Invalid URL.")
            return findings

        log_info(f"Checking TLS configuration: {hostname}")

        context = ssl.create_default_context()

        with socket.create_connection(
            (hostname, port),
            timeout=10
        ) as connection:

            with context.wrap_socket(
                connection,
                server_hostname=hostname
            ) as secure_socket:

                certificate = secure_socket.getpeercert()

                tls_version = secure_socket.version()
                cipher = secure_socket.cipher()

                if tls_version:
                    log_info(f"TLS version detected: {tls_version}")

                if cipher:
                    log_info(f"Cipher detected: {cipher[0]}")

                expiry_date = certificate.get("notAfter")

                if expiry_date:

                    expiry = datetime.strptime(
                        expiry_date,
                        "%b %d %H:%M:%S %Y %Z"
                    )

                    remaining_days = (
                        expiry - datetime.utcnow()
                    ).days

                    if remaining_days < 0:

                        findings.append(
                            Finding(
                                target=url,
                                category="TLS",
                                severity="High",
                                description="TLS certificate has expired.",
                                evidence=f"Certificate expired on {expiry_date}.",
                                recommendation="Replace the expired TLS certificate."
                            )
                        )

                    elif remaining_days <= 30:

                        findings.append(
                            Finding(
                                target=url,
                                category="TLS",
                                severity="Medium",
                                description="TLS certificate is close to expiry.",
                                evidence=f"Certificate expires on {expiry_date}.",
                                recommendation="Renew the certificate before it expires."
                            )
                        )

        log_info("TLS check completed.")

    except ssl.SSLCertVerificationError as error:

        log_error(f"TLS certificate verification failed: {error}")

        findings.append(
            Finding(
                target=url,
                category="TLS",
                severity="High",
                description="TLS certificate verification failed.",
                evidence=str(error),
                recommendation="Check that the certificate is valid, trusted, and correctly configured."
            )
        )

    except (socket.timeout, socket.error) as error:

        log_error(f"TLS connection failed: {error}")

    except ValueError as error:

        log_error(f"TLS check error: {error}")

    except Exception as error:

        log_error(f"Unexpected TLS error: {error}")

    return findings