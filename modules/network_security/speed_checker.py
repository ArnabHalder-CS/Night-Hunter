# ============================================================
# NIGHT HUNTER - Real Target Socket Reconnaissance Engine
# ============================================================
# 100% Pure Python standard library (socket, time, urllib).
# Zero mock data. Real socket probes, PTR lookups, and banner grabbing.
# Works identically across Windows, Kali Linux, Termux (Android), and macOS.

import socket
import time
import urllib.parse
from datetime import datetime

COMMON_AUDIT_PORTS = [
    (21, "FTP", "File Transfer Protocol", "High"),
    (22, "SSH", "Secure Shell Remote Access", "Low"),
    (23, "Telnet", "Unencrypted Remote Terminal", "Critical"),
    (25, "SMTP", "Simple Mail Transfer", "Medium"),
    (53, "DNS", "Domain Name System", "Low"),
    (80, "HTTP", "World Wide Web HTTP", "Low"),
    (110, "POP3", "Post Office Protocol", "Medium"),
    (139, "NetBIOS", "NetBIOS Session Service", "High"),
    (143, "IMAP", "Internet Message Access", "Medium"),
    (443, "HTTPS", "Secure HTTP (TLS/SSL)", "Low"),
    (445, "SMB", "Direct SMB / WannaCry Vector", "Critical"),
    (3306, "MySQL", "MySQL Database Service", "High"),
    (3389, "RDP", "Remote Desktop Protocol", "High"),
    (8080, "HTTP-Proxy", "Alternative Web Port / Proxy", "Low"),
]


def scan_target_network(target: str) -> dict:
    """Perform authentic socket-based reconnaissance against target IP or hostname."""
    clean_target = (target or "").strip()
    if clean_target.startswith(("http://", "https://")):
        parsed = urllib.parse.urlparse(clean_target)
        clean_target = parsed.hostname or clean_target

    if not clean_target:
        return {
            "success": False,
            "error": "Target IP address or hostname is required."
        }

    # 1. Resolve Target IP
    try:
        target_ip = socket.gethostbyname(clean_target)
    except Exception as dns_err:
        return {
            "success": False,
            "error": f"Failed to resolve target '{clean_target}': {dns_err}"
        }

    # 2. Reverse DNS (PTR Record)
    try:
        hostnames = socket.gethostbyaddr(target_ip)
        ptr_record = hostnames[0] if hostnames else "No PTR Record"
    except Exception:
        ptr_record = "No PTR Record / Reverse DNS Not Configured"

    # 3. ICMP/TCP Latency & Jitter (4 samples on standard ports)
    latencies = []
    for _ in range(4):
        t0 = time.time()
        probed = False
        for probe_port in [443, 80, 53, 22]:
            try:
                s_probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_probe.settimeout(0.8)
                code = s_probe.connect_ex((target_ip, probe_port))
                s_probe.close()
                if code == 0:
                    latencies.append((time.time() - t0) * 1000)
                    probed = True
                    break
            except Exception:
                pass
        if not probed:
            try:
                s_fb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_fb.settimeout(0.8)
                s_fb.connect_ex((target_ip, 80))
                s_fb.close()
                latencies.append((time.time() - t0) * 1000)
            except Exception:
                pass

    if latencies:
        avg_latency = round(sum(latencies) / len(latencies), 1)
        jitter = round(max(latencies) - min(latencies), 1) if len(latencies) > 1 else 0
        status = "ONLINE / REACHABLE"
        loss = "0%"
    else:
        avg_latency = 0
        jitter = 0
        status = "FILTERED / HOST OFFLINE"
        loss = "100%"

    # 4. Port-by-Port Real Socket Scanning & Banner Grabbing
    open_ports = []
    closed_ports = []

    for port, service, desc, risk in COMMON_AUDIT_PORTS:
        t0 = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8)
        code = sock.connect_ex((target_ip, port))
        latency_ms = round((time.time() - t0) * 1000, 1)

        banner = ""
        if code == 0:
            # Attempt non-intrusive banner grab
            try:
                if port in [21, 22, 25, 110]:
                    banner = sock.recv(256).decode(errors="ignore").strip()
                elif port in [80, 8080]:
                    sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                    raw = sock.recv(256).decode(errors="ignore").strip()
                    banner = raw.splitlines()[0] if raw else ""
            except Exception:
                banner = ""

            open_ports.append({
                "port": port,
                "service": service,
                "desc": desc,
                "risk": risk,
                "state": "OPEN",
                "latency_ms": latency_ms,
                "banner": banner
            })
        else:
            closed_ports.append({
                "port": port,
                "service": service,
                "desc": desc,
                "risk": risk,
                "state": "CLOSED / FILTERED",
                "latency_ms": latency_ms,
                "banner": ""
            })
        sock.close()

    # 5. Security Posture & Vulnerability Analysis
    score = 100
    risk_flags = []

    # Check unencrypted protocols
    telnet_open = any(p["port"] == 23 for p in open_ports)
    if telnet_open:
        score -= 25
        risk_flags.append({
            "severity": "CRITICAL",
            "title": "Telnet (Port 23) Exposed",
            "detail": "Unencrypted Telnet service detected. Passwords and commands are transmitted in cleartext."
        })

    ftp_open = any(p["port"] == 21 for p in open_ports)
    if ftp_open:
        score -= 15
        risk_flags.append({
            "severity": "HIGH",
            "title": "Cleartext FTP (Port 21) Open",
            "detail": "Standard FTP does not encrypt credentials. Recommend migrating to SFTP (Port 22)."
        })

    smb_open = any(p["port"] == 445 for p in open_ports)
    if smb_open:
        score -= 20
        risk_flags.append({
            "severity": "CRITICAL",
            "title": "SMB Service (Port 445) Exposed",
            "detail": "Port 445 open. High vulnerability to EternalBlue, NTLM relay attacks, and lateral movement."
        })

    mysql_open = any(p["port"] == 3306 for p in open_ports)
    if mysql_open:
        score -= 15
        risk_flags.append({
            "severity": "HIGH",
            "title": "Database Listener (Port 3306) Exposed",
            "detail": "MySQL database port is accessible over the network. Recommend binding to localhost (127.0.0.1) or firewalling."
        })

    rdp_open = any(p["port"] == 3389 for p in open_ports)
    if rdp_open:
        score -= 15
        risk_flags.append({
            "severity": "MEDIUM",
            "title": "RDP (Port 3389) Reachable",
            "detail": "Remote Desktop accessible. Ensure Network Level Authentication (NLA) and brute-force lockouts are enforced."
        })

    if not open_ports and status.startswith("ONLINE"):
        score = 95
        risk_flags.append({
            "severity": "GOOD",
            "title": "Hardened Attack Surface",
            "detail": "Host is online but all standard audit ports are closed or firewalled."
        })
    elif open_ports and not risk_flags:
        risk_flags.append({
            "severity": "GOOD",
            "title": "Standard Service Exposure",
            "detail": f"Host exposes {len(open_ports)} standard service(s) (e.g. HTTP/HTTPS/DNS) with no critical legacy ports open."
        })

    if score >= 85:
        posture_grade = "HARDENED / SECURE"
        grade_color = "#4ade80"
    elif score >= 65:
        posture_grade = "MODERATE EXPOSURE"
        grade_color = "#38bdf8"
    else:
        posture_grade = "HIGH RISK / VULNERABLE"
        grade_color = "#f87171"

    all_ports = open_ports + closed_ports

    return {
        "success": True,
        "target": clean_target,
        "target_ip": target_ip,
        "ptr_record": ptr_record,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "latency_telemetry": {
            "avg_latency_ms": avg_latency,
            "jitter_ms": jitter,
            "packet_loss": loss,
            "status": status,
        },
        "open_ports": open_ports,
        "closed_ports": closed_ports,
        "all_ports": all_ports,
        "total_open_ports": len(open_ports),
        "total_scanned_ports": len(COMMON_AUDIT_PORTS),
        "security_posture": {
            "defense_score": max(score, 0),
            "posture_grade": posture_grade,
            "grade_color": grade_color,
            "risk_flags": risk_flags
        },
        # Compatibility fields
        "host_check": {
            "reachable": bool(latencies or open_ports),
            "response_time_ms": avg_latency,
            "jitter_ms": jitter,
            "connection_strength": "EXCELLENT" if avg_latency < 50 else "GOOD",
            "packet_loss": loss,
            "status": status
        }
    }


def test_network_connection(target: str = "", mode: str = "") -> dict:
    """Wrapper function preserving API route contract."""
    clean_target = (target or "").strip()
    if not clean_target:
        return {
            "success": False,
            "error": "Please enter a target IP address or hostname to initiate scan."
        }
    return scan_target_network(clean_target)
