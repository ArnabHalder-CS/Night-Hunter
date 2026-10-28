# ============================================================
# NIGHT HUNTER - Network Security Checker
# ============================================================
# Defensive network information and security checking module.
#
# This file provides reusable functions for:
# - Local network information
# - Host resolution
# - Host reachability
# - TCP port checking
# - Common port scanning
# - Service identification
# - Connectivity testing
#
# Designed to work with:
#     network_security/pentest.py
#     network_security/load_benchmark.py
#
# ============================================================

import socket
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.logger import log_info, log_warning, log_error
from core.validators import safe_host
from modules.network_security.device_scanner import (
    get_device_recon,
    scan_target_nmap,
    scan_target_native,
    COMMON_UDP_PORTS,
    LAN_CAUTION,
)




# ============================================================
# CONSTANTS
# ============================================================

# Full common-service checks remain thorough, but port probes run concurrently
# below so a filtered host does not make the interface appear frozen.
DEFAULT_TIMEOUT = 1.5
MAX_SCAN_WORKERS = 12

COMMON_PORTS = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    67: "DHCP-SERVER",
    68: "DHCP-CLIENT",
    80: "HTTP",
    110: "POP3",
    111: "RPCBIND",
    119: "NNTP",
    123: "NTP",
    135: "MS-RPC",
    139: "NETBIOS",
    143: "IMAP",
    161: "SNMP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    587: "SMTP-SUBMISSION",
    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "ORACLE",
    2049: "NFS",
    2375: "DOCKER",
    2376: "DOCKER-TLS",
    3306: "MYSQL",
    3389: "RDP",
    5432: "POSTGRESQL",
    5900: "VNC",
    6379: "REDIS",
    8080: "HTTP-ALT",
    8443: "HTTPS-ALT",
    9200: "ELASTICSEARCH",
    27017: "MONGODB"
}


# ============================================================
# BASIC HELPERS
# ============================================================

def get_timestamp():
    """Return the current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_host(host):
    """
    Clean, sanitize, and strictly validate a hostname or IP address.
    Prevents option injection (e.g. -f, --script=...) and invalid characters.
    """
    return safe_host(host)


def get_service_name(port):
    """Return the known service name for a port."""

    try:
        port = int(port)
    except (TypeError, ValueError):
        return "UNKNOWN"

    if port in COMMON_PORTS:
        return COMMON_PORTS[port]

    try:
        return socket.getservbyport(port, "tcp").upper()
    except (OSError, socket.error):
        return "UNKNOWN"


# ============================================================
# LOCAL NETWORK INFORMATION
# ============================================================

def get_network_info(target=None):
    """
    Collect device recon and network information for a target host/IP.
    If target is specified, performs Nmap-style targeted intelligence
    (device name, OS model, MAC address, open TCP and UDP ports).
    """
    if target:
        return get_device_recon(target)

    """
    Collect basic information about the local machine/network.

    Returns:
        Dictionary containing hostname, local IP, platform,
        operating system and timestamp.
    """

    info = {
        "hostname": None,
        "ip_address": None,
        "platform": platform.system(),
        "system": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "timestamp": get_timestamp()
    }

    try:
        hostname = socket.gethostname()
        info["hostname"] = hostname

        try:
            local_ip = socket.gethostbyname(hostname)
            info["ip_address"] = local_ip
        except socket.gaierror:
            info["ip_address"] = "Unable to resolve"

        log_info("Network information collected.")

    except Exception as error:
        log_error(f"Unable to collect network information: {error}")

    return info


# ============================================================
# DNS / HOST RESOLUTION
# ============================================================

def resolve_host(host):
    """
    Resolve a hostname to IP addresses.

    Returns:
        Dictionary containing hostname and resolved addresses.
    """

    host = clean_host(host)

    result = {
        "host": host,
        "resolved": False,
        "addresses": [],
        "error": None
    }

    if not host:
        result["error"] = "Host is empty."
        return result

    try:
        records = socket.getaddrinfo(
            host,
            None,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )

        addresses = []

        for record in records:
            address = record[4][0]

            if address not in addresses:
                addresses.append(address)

        result["addresses"] = addresses
        result["resolved"] = bool(addresses)

        if result["resolved"]:
            log_info(
                f"Host resolved: {host} -> "
                f"{', '.join(addresses)}"
            )
        else:
            log_warning(f"No IP address found for {host}")

    except socket.gaierror as error:
        result["error"] = str(error)
        log_error(f"Unable to resolve host {host}: {error}")

    except Exception as error:
        result["error"] = str(error)
        log_error(f"Host resolution failed: {error}")

    return result


# ============================================================
# SIMPLE HOST CHECK
# ============================================================

def check_host(host):
    """
    Check whether a host can be resolved.

    This is a lightweight check.
    It does not perform an aggressive network scan.
    """

    host = clean_host(host)

    result = {
        "host": host,
        "reachable": False,
        "addresses": [],
        "error": None
    }

    if not host:
        result["error"] = "Host is empty."
        return result

    resolution = resolve_host(host)

    result["addresses"] = resolution["addresses"]

    if resolution["resolved"]:
        result["reachable"] = True
        log_info(f"Host is reachable/resolvable: {host}")
    else:
        result["error"] = resolution["error"]

    return result


# ============================================================
# TCP PORT CHECK
# ============================================================

def check_port(host, port, timeout=DEFAULT_TIMEOUT):
    """
    Check a single TCP port.

    Returns:
        Dictionary containing host, port, state and service.

    States:
        OPEN
        CLOSED
        FILTERED
        ERROR
    """

    host = clean_host(host)

    result = {
        "host": host,
        "port": port,
        "state": "ERROR",
        "service": get_service_name(port),
        "response_time": None,
        "error": None
    }

    if not host:
        result["error"] = "Host is empty."
        return result

    try:
        port = int(port)
    except (TypeError, ValueError):
        result["error"] = "Invalid port number."
        return result

    if port < 1 or port > 65535:
        result["error"] = "Port must be between 1 and 65535."
        return result

    try:
        start = datetime.now()

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(float(timeout))

        connection = sock.connect_ex((host, port))

        elapsed = datetime.now() - start

        result["response_time"] = round(
            elapsed.total_seconds() * 1000,
            2
        )

        sock.close()

        if connection == 0:
            result["state"] = "OPEN"

            log_info(
                f"{host}:{port} OPEN "
                f"({result['service']})"
            )

        elif connection in {
            10061,
            111,
            61
        }:
            result["state"] = "CLOSED"

        else:
            result["state"] = "FILTERED"

    except socket.timeout:
        result["state"] = "FILTERED"

    except socket.gaierror as error:
        result["state"] = "ERROR"
        result["error"] = str(error)

    except OSError as error:
        result["state"] = "ERROR"
        result["error"] = str(error)

    except Exception as error:
        result["state"] = "ERROR"
        result["error"] = str(error)

    return result


# ============================================================
# COMMON PORT SCAN
# ============================================================

def scan_common_ports(host, timeout=DEFAULT_TIMEOUT):
    """
    Scan a predefined list of common TCP ports.

    This function is intended for security checking and
    authorized testing.
    """

    host = clean_host(host)

    results = []

    if not host:
        log_error("Cannot scan an empty host.")
        return results

    log_info(f"Scanning common ports on {host}")

    # Run a small, bounded set of independent TCP checks in parallel. This is
    # still limited to the defined common-port list and is intended only for
    # authorized defensive checks, but it avoids making the web interface look
    # frozen when a firewall silently drops packets.
    with ThreadPoolExecutor(
        max_workers=min(MAX_SCAN_WORKERS, len(COMMON_PORTS))
    ) as executor:
        checks = {
            port: executor.submit(
                check_port,
                host,
                port,
                timeout
            )
            for port in COMMON_PORTS
        }

        # Preserve the familiar port order in the final report.
        for port in COMMON_PORTS:
            try:
                results.append(checks[port].result())
            except Exception as error:
                results.append({
                    "host": host,
                    "port": port,
                    "state": "ERROR",
                    "service": get_service_name(port),
                    "response_time": None,
                    "error": str(error)
                })

    open_ports = [
        item for item in results
        if item["state"] == "OPEN"
    ]

    log_info(
        f"Port scan completed. "
        f"{len(open_ports)} open port(s) found."
    )

    return results


# ============================================================
# OPEN PORT ONLY
# ============================================================

def get_open_ports(host, timeout=DEFAULT_TIMEOUT):
    """
    Return only open ports from the common port scan.
    """

    results = scan_common_ports(
        host,
        timeout=timeout
    )

    return [
        result
        for result in results
        if result["state"] == "OPEN"
    ]


# ============================================================
# SERVICE CHECK
# ============================================================

def check_common_services(host, timeout=DEFAULT_TIMEOUT):
    """
    Check common services and return only services that
    respond on TCP.
    """

    open_ports = get_open_ports(
        host,
        timeout=timeout
    )

    services = []

    for result in open_ports:

        services.append({
            "port": result["port"],
            "service": result["service"],
            "state": result["state"],
            "response_time": result["response_time"]
        })

    return services


# ============================================================
# SERVICE BANNER
# ============================================================

def grab_banner(host, port, timeout=3):
    """
    Attempt a very small service banner check.

    This is intentionally lightweight. It sends a minimal
    request and reads the first available response.

    Returns:
        Dictionary with banner information.
    """

    host = clean_host(host)

    result = {
        "host": host,
        "port": port,
        "service": get_service_name(port),
        "banner": None,
        "success": False,
        "error": None
    }

    try:
        port = int(port)
    except (TypeError, ValueError):
        result["error"] = "Invalid port."
        return result

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(float(timeout))

        connection = sock.connect_ex(
            (host, port)
        )

        if connection != 0:
            sock.close()
            result["error"] = "Port is not open."
            return result

        # Some services respond immediately.
        # For HTTP, send a small HEAD request.
        if port in {80, 8080, 8000, 8888}:

            request = (
                f"HEAD / HTTP/1.0\r\n"
                f"Host: {host}\r\n"
                f"Connection: close\r\n\r\n"
            )

            sock.sendall(
                request.encode(
                    "utf-8",
                    errors="ignore"
                )
            )

        try:

            data = sock.recv(1024)

            if data:
                banner = data.decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                result["banner"] = banner[:500]
                result["success"] = True

        except socket.timeout:
            result["banner"] = "No banner received."

        sock.close()

    except Exception as error:
        result["error"] = str(error)

    return result


# ============================================================
# HTTP CONNECTIVITY TEST
# ============================================================

def connectivity_test(host, port=80, timeout=3):
    """
    Test basic TCP connectivity to a host.

    Returns True when the TCP connection succeeds.
    """

    host = clean_host(host)

    if not host:
        log_error("Connectivity test failed: empty host.")
        return False

    try:

        sock = socket.create_connection(
            (host, int(port)),
            timeout=float(timeout)
        )

        sock.close()

        log_info(
            f"Connectivity test successful: "
            f"{host}:{port}"
        )

        return True

    except Exception as error:

        log_warning(
            f"Connectivity test failed: "
            f"{host}:{port} - {error}"
        )

        return False


# ============================================================
# PING-LIKE TEST
# ============================================================

def ping_host(host, timeout=2):
    """
    Perform a basic operating-system ping.

    Returns:
        Dictionary containing success and output.

    Note:
        Windows and Unix-like systems use different ping
        command arguments, so the command is selected
        according to the operating system.
    """

    host = clean_host(host)

    result = {
        "host": host,
        "success": False,
        "output": "",
        "error": None
    }

    if not host:
        result["error"] = "Host is empty."
        return result

    try:

        system = platform.system().lower()

        if system == "windows":

            command = [
                "ping",
                "-n",
                "1",
                "-w",
                str(int(timeout * 1000)),
                host
            ]

        else:

            command = [
                "ping",
                "-c",
                "1",
                "-W",
                str(int(timeout)),
                host
            ]

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=float(timeout) + 2
        )

        output = (
            process.stdout
            if process.stdout
            else process.stderr
        )

        result["output"] = output.strip()[:2000]

        if process.returncode == 0:

            result["success"] = True

            log_info(
                f"Ping successful: {host}"
            )

        else:

            log_warning(
                f"Ping failed: {host}"
            )

    except subprocess.TimeoutExpired:

        result["error"] = "Ping timed out."

    except FileNotFoundError:

        result["error"] = (
            "Ping command is not available "
            "on this system."
        )

    except Exception as error:

        result["error"] = str(error)

    return result


# ============================================================
# NETWORK SUMMARY
# ============================================================

def get_network_summary(host):
    """
    Produce a compact network security summary.

    This combines:
        - DNS resolution
        - host check
        - common port scan
        - open service identification
    """

    host = clean_host(host)
    recon = get_device_recon(host) if host else {}

    summary = {
        "target": host,
        "device_name": recon.get("device_name", "Unknown"),
        "os_model": recon.get("os_model", "Unknown OS"),
        "device_type": recon.get("device_type", "general purpose"),
        "mac_address": recon.get("mac_address"),
        "mac_vendor": recon.get("mac_vendor", ""),
        "udp_ports": recon.get("udp_ports", []),
        "caution": recon.get("caution", LAN_CAUTION),
        "scan_engine": recon.get("scan_engine", "Nmap Engine"),
        "runtime_mode": recon.get("runtime_mode", "local"),
        "capabilities": recon.get("capabilities", {}),
        "timestamp": get_timestamp(),
        "resolution": None,
        "host_check": None,
        "open_ports": [],
        "open_services": [],
        "service_banners": [],
        "total_open_ports": 0
    }

    if not host:
        return summary

    summary["resolution"] = resolve_host(host)

    summary["host_check"] = check_host(host)

    scan_results = scan_common_ports(host)

    summary["open_ports"] = [
        result
        for result in scan_results
        if result["state"] == "OPEN"
    ]

    summary["open_services"] = [
        {
            "port": result["port"],
            "service": result["service"],
            "response_time": result["response_time"]
        }
        for result in summary["open_ports"]
    ]

    # Add small, protocol-aware banners for responding HTTP services. This
    # enriches an authorized defensive scan without sending exploit payloads.
    http_ports = [
        result["port"]
        for result in summary["open_ports"]
        if result["port"] in {80, 8080, 8000, 8888}
    ]

    if http_ports:
        with ThreadPoolExecutor(
            max_workers=min(4, len(http_ports))
        ) as executor:
            futures = [
                executor.submit(grab_banner, host, port, 2)
                for port in http_ports
            ]
            summary["service_banners"] = [
                future.result()
                for future in futures
            ]

    recon = get_device_recon(host)
    summary["device_name"] = recon.get("device_name", "Unknown")
    summary["os_model"] = recon.get("os_model", "Unknown OS")
    summary["device_type"] = recon.get("device_type", "general purpose")
    summary["mac_address"] = recon.get("mac_address")
    summary["mac_vendor"] = recon.get("mac_vendor", "")
    summary["udp_ports"] = recon.get("udp_ports", [])
    summary["caution"] = recon.get("caution", LAN_CAUTION)
    summary["scan_engine"] = recon.get("scan_engine", "Nmap Engine")
    summary["runtime_mode"] = recon.get("runtime_mode", "local")
    summary["capabilities"] = recon.get("capabilities", {})
    summary["total_open_ports"] = len(summary["open_ports"]) + sum(
        port.get("state") == "OPEN" for port in summary["udp_ports"]
    )
    summary["indeterminate_udp_ports"] = sum(
        port.get("state") != "OPEN" for port in summary["udp_ports"]
    )

    return summary


# ============================================================
# DISPLAY HELPERS
# ============================================================

def display_network_info(info):
    """Display local network information."""

    print()
    print("=" * 60)
    print("NETWORK INFORMATION")
    print("=" * 60)

    print(f"Hostname : {info.get('hostname')}")
    print(f"IP       : {info.get('ip_address')}")
    print(f"Platform : {info.get('platform')}")
    print(f"System   : {info.get('system')}")
    print(f"Machine  : {info.get('machine')}")
    print(f"Time     : {info.get('timestamp')}")

    print("=" * 60)


def display_port_results(results):
    """Display port scan results."""

    print()
    print("=" * 60)
    print("PORT SCAN RESULTS")
    print("=" * 60)

    if not results:
        print("No results.")
        return

    for result in results:

        port = result.get("port")
        service = result.get("service")
        state = result.get("state")
        response = result.get("response_time")

        print(
            f"{port:<6} "
            f"{service:<18} "
            f"{state:<10} "
            f"{response} ms"
        )

    print("=" * 60)


# ============================================================
# MAIN CHECKER FUNCTION
# ============================================================

def run_network_check(host):
    """
    Main reusable entry point for Network Security Checker.

    Returns:
        Complete network-check dictionary.
    """

    host = clean_host(host)

    if not host:

        log_error(
            "Network check cannot start "
            "without a target."
        )

        return {
            "target": "",
            "success": False,
            "error": "Target is empty."
        }

    log_info(
        f"Starting network security check: {host}"
    )

    summary = get_network_summary(host)

    summary["success"] = True

    log_info(
        f"Network security check completed: {host}"
    )

    return summary


# ============================================================
# LIVE NETWORK CHECK
# ============================================================

def iter_network_check(host, timeout=DEFAULT_TIMEOUT):
    """Yield progress events for an authorized advanced network scan.

    Each port result is yielded as soon as its TCP check finishes so user
    interfaces can show real work instead of appearing frozen until the final
    report is ready.
    """

    host = clean_host(host)

    if not host:
        yield {
            "type": "error",
            "message": "Target is empty."
        }
        return

    yield {
        "type": "started",
        "target": host,
        "total_ports": len(COMMON_PORTS)
    }

    resolution = resolve_host(host)
    yield {
        "type": "resolution",
        "resolution": resolution
    }

    host_check = check_host(host)
    yield {
        "type": "host_check",
        "host_check": host_check
    }
    recon = get_device_recon(host)
    yield {
        "type": "device_info",
        "device": recon
    }

    scan_results = []
    with ThreadPoolExecutor(
        max_workers=min(MAX_SCAN_WORKERS, len(COMMON_PORTS))
    ) as executor:
        futures = {
            executor.submit(check_port, host, port, timeout): port
            for port in COMMON_PORTS
        }

        for completed, future in enumerate(
            as_completed(futures),
            start=1
        ):
            port = futures[future]

            try:
                result = future.result()
            except Exception as error:
                result = {
                    "host": host,
                    "port": port,
                    "state": "ERROR",
                    "service": get_service_name(port),
                    "response_time": None,
                    "error": str(error)
                }

            scan_results.append(result)
            yield {
                "type": "port",
                "completed": completed,
                "total_ports": len(COMMON_PORTS),
                "port_result": result
            }

    order = {
        port: index
        for index, port in enumerate(COMMON_PORTS)
    }
    scan_results.sort(
        key=lambda item: order.get(item["port"], 99999)
    )

    open_ports = [
        result for result in scan_results
        if result["state"] == "OPEN"
    ]

    service_banners = []
    http_ports = [
        result["port"] for result in open_ports
        if result["port"] in {80, 8080, 8000, 8888}
    ]

    if http_ports:
        with ThreadPoolExecutor(
            max_workers=min(4, len(http_ports))
        ) as executor:
            banner_futures = {
                executor.submit(grab_banner, host, port, 2): port
                for port in http_ports
            }

            for future in as_completed(banner_futures):
                banner = future.result()
                service_banners.append(banner)
                yield {
                    "type": "banner",
                    "banner": banner
                }

    summary = {
        "target": host,
        "device_name": recon.get("device_name", "Unknown"),
        "os_model": recon.get("os_model", "Unknown OS"),
        "device_type": recon.get("device_type", "general purpose"),
        "mac_address": recon.get("mac_address"),
        "mac_vendor": recon.get("mac_vendor", ""),
        "udp_ports": recon.get("udp_ports", []),
        "caution": recon.get("caution", LAN_CAUTION),
        "scan_engine": recon.get("scan_engine", "Nmap Engine"),
        "runtime_mode": recon.get("runtime_mode", "local"),
        "capabilities": recon.get("capabilities", {}),
        "timestamp": get_timestamp(),
        "resolution": resolution,
        "host_check": host_check,
        "open_ports": open_ports,
        "open_services": [
            {
                "port": result["port"],
                "service": result["service"],
                "response_time": result["response_time"]
            }
            for result in open_ports
        ],
        "service_banners": service_banners,
        "total_open_ports": len(open_ports) + sum(
            port.get("state") == "OPEN" for port in recon.get("udp_ports", [])
        ),
        "indeterminate_udp_ports": sum(
            port.get("state") != "OPEN" for port in recon.get("udp_ports", [])
        ),
        "success": True
    }

    yield {
        "type": "complete",
        "result": summary
    }


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("NIGHT HUNTER - NETWORK SECURITY CHECKER")
    print("=" * 60)

    target = input(
        "\nEnter host or IP to check: "
    ).strip()

    if not target:

        print(
            "\n[!] No target entered."
        )

    else:

        print(
            "\n[*] Collecting network information..."
        )

        info = get_network_info()

        display_network_info(info)

        print(
            "\n[*] Running target check..."
        )

        result = run_network_check(target)

        print()
        print(
            f"Target: {result.get('target')}"
        )

        print(
            f"Resolved: "
            f"{result.get('resolution', {}).get('resolved')}"
        )

        addresses = result.get(
            "resolution",
            {}
        ).get(
            "addresses",
            []
        )

        if addresses:

            print(
                "Addresses: "
                + ", ".join(addresses)
            )

        open_ports = result.get(
            "open_ports",
            []
        )

        print(
            f"Open common ports: "
            f"{len(open_ports)}"
        )

        if open_ports:

            display_port_results(
                result.get(
                    "open_ports",
                    []
                )
            )

        print()
        print(
            "[+] Network checker completed."
        )
