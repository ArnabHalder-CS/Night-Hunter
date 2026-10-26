# ============================================================
# NIGHT HUNTER - Network Speed, Strength & Basic Checker
# ============================================================
# Provides latency testing, connection strength rating, network speed,
# and basic connectivity checking without aggressive port sweeps or Nmap.

import socket
import time
import urllib.request
import urllib.parse
from datetime import datetime
from core.logger import log_info, log_error

STANDARD_PORTS = {
    80: "HTTP Web Service",
    443: "HTTPS Secure Web",
    53: "DNS Name Resolution",
    22: "SSH Remote Access",
}


def test_network_connection(target: str) -> dict:
    """Run a clean network connectivity, speed, and strength audit."""
    host = target.strip()
    if host.startswith(("http://", "https://")):
        parsed = urllib.parse.urlparse(host)
        host = parsed.hostname or host

    summary = {
        "success": True,
        "target": host,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resolution": {
            "hostname": host,
            "ip_address": "",
            "addresses": [],
            "resolved": False
        },
        "host_check": {
            "reachable": False,
            "response_time_ms": 0,
            "jitter_ms": 0,
            "connection_strength": "OFFLINE",
            "packet_loss": "100%",
            "status": "UNREACHABLE"
        },
        "speed_test": {
            "download_speed_mbps": 0.0,
            "speed_label": "Testing...",
            "ttfb_ms": 0,
            "grade": "Standard"
        },
        "open_ports": [],
        "open_services": [],
        "total_open_ports": 0
    }

    # 1. DNS Resolution
    primary_ip = host
    try:
        addr_info = socket.getaddrinfo(host, None)
        ips = sorted(list(set(item[4][0] for item in addr_info if item[4])))
        summary["resolution"]["addresses"] = ips
        if ips:
            summary["resolution"]["ip_address"] = ips[0]
            summary["resolution"]["resolved"] = True
            primary_ip = ips[0]
    except Exception as dns_err:
        log_error(f"DNS lookup failed for {host}: {dns_err}")

    # 2. Connection Strength & Latency Test (3 samples)
    latencies = []
    test_port = 443 if "." in host else 80

    for _ in range(3):
        t0 = time.time()
        try:
            s = socket.create_connection((primary_ip, test_port), timeout=2.0)
            s.close()
            latencies.append((time.time() - t0) * 1000)
        except Exception:
            try:
                t0_fb = time.time()
                s = socket.create_connection((primary_ip, 80), timeout=2.0)
                s.close()
                latencies.append((time.time() - t0_fb) * 1000)
            except Exception:
                pass

    if latencies:
        avg_lat = round(sum(latencies) / len(latencies), 1)
        jitter = round(max(latencies) - min(latencies), 1) if len(latencies) > 1 else 0

        if avg_lat < 50:
            strength = "EXCELLENT"
        elif avg_lat < 120:
            strength = "GOOD"
        elif avg_lat < 250:
            strength = "FAIR"
        else:
            strength = "POOR"

        summary["host_check"] = {
            "reachable": True,
            "response_time_ms": avg_lat,
            "jitter_ms": jitter,
            "connection_strength": strength,
            "packet_loss": "0%",
            "status": "ONLINE"
        }
    else:
        if summary["resolution"]["addresses"]:
            summary["host_check"]["reachable"] = True
            summary["host_check"]["connection_strength"] = "RESOLVED"
            summary["host_check"]["status"] = "HOST RESOLVED"
            summary["host_check"]["packet_loss"] = "Filtered"

    # 3. Basic Non-Intrusive Service Checks
    open_port_items = []
    for port, service_name in STANDARD_PORTS.items():
        t0 = time.time()
        try:
            with socket.create_connection((primary_ip, port), timeout=1.2) as sock:
                r_time = round((time.time() - t0) * 1000, 1)
                open_port_items.append({
                    "port": port,
                    "service": service_name,
                    "state": "OPEN",
                    "response_time": r_time
                })
        except Exception:
            pass

    summary["open_ports"] = open_port_items
    summary["open_services"] = open_port_items
    summary["total_open_ports"] = len(open_port_items)

    # 4. Network Speed Check (Throughput in Mbps)
    try:
        speed_url = "https://speed.cloudflare.com/__down?bytes=1048576"
        t0_speed = time.time()
        req = urllib.request.Request(speed_url, headers={"User-Agent": "NightHunter/2.0 NetworkSpeedCheck"})
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            data = resp.read()
            duration = time.time() - t0_speed
            if duration > 0 and len(data) > 0:
                mbps = round((len(data) * 8) / (duration * 1_000_000), 2)
                summary["speed_test"] = {
                    "download_speed_mbps": mbps,
                    "speed_label": f"{mbps} Mbps",
                    "ttfb_ms": round(summary["host_check"]["response_time_ms"], 1),
                    "grade": "High Speed" if mbps > 25 else "Moderate Speed"
                }
    except Exception:
        avg = summary["host_check"]["response_time_ms"]
        est = round(max(5.0, 1000 / (avg if avg > 0 else 50)), 1)
        summary["speed_test"] = {
            "download_speed_mbps": est,
            "speed_label": f"~{est} Mbps (Est.)",
            "ttfb_ms": round(avg, 1),
            "grade": "Standard"
        }

    return summary
