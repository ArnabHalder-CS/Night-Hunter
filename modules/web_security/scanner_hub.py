"""Local, authorised adapters for third-party web scanners.

Night Hunter never pretends a third-party scanner is installed.  Nikto and
Nuclei run only when their CLI is available on the computer running the local
server.  Nessus and Acunetix are commercial products and must be connected to
the user's own licensed deployment; they are intentionally not bundled here.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from html import escape
from urllib.parse import urlparse
from xml.etree import ElementTree


MAX_OUTPUT = 750_000


def _runtime_is_cloud() -> bool:
    return os.environ.get("NIGHT_HUNTER_RUNTIME", "").lower() == "cloud"


def scanner_status() -> dict:
    """Describe which integrations can genuinely run on this host."""
    cloud = _runtime_is_cloud()
    nikto_path = shutil.which("nikto") or shutil.which("nikto.pl")
    nuclei_path = shutil.which("nuclei")
    gvm_path = shutil.which("gvm-cli") or shutil.which("gvm-cli.exe")
    gvm_enabled = os.environ.get("NIGHT_HUNTER_GVM_ENABLED", "").lower() in {"1", "true", "yes"}
    return {
        "runtime": "cloud" if cloud else "local",
        "scanners": {
            "night_hunter": {
                "name": "Night Hunter authorised audit",
                "available": True,
                "kind": "built-in",
                "description": "Headers, TLS, cookies, methods, public endpoints, technology and safe indicators.",
            },
            "nikto": {
                "name": "Nikto",
                "available": bool(nikto_path) and not cloud,
                "kind": "local-cli",
                "path": nikto_path,
                "description": "Local web-server configuration and known-file audit.",
                "setup": "Install Nikto locally and ensure nikto is available in PATH.",
            },
            "nuclei": {
                "name": "Nuclei",
                "available": bool(nuclei_path) and not cloud,
                "kind": "local-cli",
                "path": nuclei_path,
                "description": "Local template-based exposure checks using the templates installed on your computer.",
                "setup": "Install Nuclei locally, update only trusted templates, and ensure nuclei is available in PATH.",
            },
            "openvas": {
                "name": "OpenVAS / Greenbone",
                "available": bool(gvm_path) and gvm_enabled and not cloud,
                "kind": "local-gmp",
                "path": gvm_path,
                "description": "Starts an authorised Full and Fast vulnerability scan through your local Greenbone service.",
                "setup": "Install and configure Greenbone/OpenVAS plus gvm-tools first, then set NIGHT_HUNTER_GVM_ENABLED=1. Credentials stay in your gvm-tools configuration, never in Night Hunter.",
            },
        },
    }


def _validate_target(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a complete http:// or https:// target URL.")
    return target


def _run_command(command: list[str], timeout: int) -> tuple[int, str, str]:
    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,
    )
    return process.returncode, process.stdout[-MAX_OUTPUT:], process.stderr[-80_000:]


def _gvm_xml(gvm_path: str, command_xml: str) -> ElementTree.Element:
    """Send one GMP request through the operator's configured gvm-cli socket."""
    code, stdout, stderr = _run_command([gvm_path, "socket", "--xml", command_xml], timeout=90)
    if code != 0:
        raise RuntimeError(f"Greenbone connection failed: {stderr or stdout or 'gvm-cli returned an error.'}")
    try:
        response = ElementTree.fromstring(stdout)
    except ElementTree.ParseError as error:
        raise RuntimeError(f"Greenbone returned unreadable XML: {error}") from error
    status = response.attrib.get("status", "")
    if not status.startswith("2"):
        raise RuntimeError(response.attrib.get("status_text", "Greenbone rejected the request."))
    return response


def _run_openvas(gvm_path: str, target: str) -> dict:
    """Create and start a local OpenVAS task; task execution remains in Greenbone."""
    hostname = urlparse(target).hostname
    if not hostname:
        raise ValueError("OpenVAS requires a valid target hostname.")
    run_label = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_host = escape(hostname)
    target_response = _gvm_xml(
        gvm_path,
        f"<create_target><name>Night Hunter {safe_host} {run_label}</name><hosts>{safe_host}</hosts></create_target>",
    )
    target_id = target_response.attrib.get("id")
    if not target_id:
        raise RuntimeError("Greenbone created no target identifier.")

    # Greenbone's documented identifiers for the built-in Full and Fast profile
    # and OpenVAS scanner. They are resolved by the local Greenbone manager.
    config_id = "daba56c8-73ec-11df-a475-002264764cea"
    scanner_id = "08b69003-5fc2-4037-a479-93b440211c73"
    task_response = _gvm_xml(
        gvm_path,
        f'<create_task><name>Night Hunter OpenVAS {safe_host} {run_label}</name><target id="{target_id}"/><config id="{config_id}"/><scanner id="{scanner_id}"/></create_task>',
    )
    task_id = task_response.attrib.get("id")
    if not task_id:
        raise RuntimeError("Greenbone created no task identifier.")
    started = _gvm_xml(gvm_path, f'<start_task task_id="{task_id}"/>')
    report_id = started.findtext("report_id")
    return {
        "scanner": "openvas",
        "success": True,
        "summary": "OpenVAS task started in your local Greenbone service. Monitor it in Greenbone; results are retained there.",
        "task_id": task_id,
        "report_id": report_id,
        "target_host": hostname,
    }


def run_local_scanner(scanner: str, target: str) -> dict:
    """Run a single installed CLI integration with conservative defaults."""
    target = _validate_target(target)
    status = scanner_status()
    if _runtime_is_cloud():
        raise RuntimeError("Third-party scanners run only in the local Windows/Linux/Termux installation, not on the public cloud service.")
    if scanner not in {"nikto", "nuclei", "openvas"}:
        raise ValueError("Only Nikto, Nuclei, or OpenVAS can be launched by this local scanner hub.")
    integration = status["scanners"][scanner]
    if not integration["available"]:
        raise RuntimeError(f"{integration['name']} is not installed or is not available in PATH. {integration['setup']}")

    if scanner == "openvas":
        return _run_openvas(integration["path"], target)

    if scanner == "nikto":
        code, stdout, stderr = _run_command(
            [integration["path"], "-h", target, "-nointeractive", "-maxtime", "10m"],
            timeout=660,
        )
        return {
            "scanner": "nikto",
            "success": code in {0, 1},
            "exit_code": code,
            "summary": "Nikto completed locally. Review the native output below and validate findings manually.",
            "output": stdout,
            "warnings": stderr,
        }

    code, stdout, stderr = _run_command(
        [integration["path"], "-u", target, "-jsonl", "-silent", "-rate-limit", "10", "-timeout", "8"],
        timeout=660,
    )
    findings = []
    for line in stdout.splitlines():
        try:
            item = json.loads(line)
            findings.append({
                "template": item.get("template-id", "unknown-template"),
                "severity": item.get("info", {}).get("severity", "unknown"),
                "name": item.get("info", {}).get("name", "Nuclei finding"),
                "matched_at": item.get("matched-at", item.get("host", target)),
            })
        except json.JSONDecodeError:
            continue
    return {
        "scanner": "nuclei",
        "success": code == 0,
        "exit_code": code,
        "summary": f"Nuclei completed locally with {len(findings)} parsed finding(s). Templates determine coverage.",
        "findings": findings,
        "output": stdout,
        "warnings": stderr,
    }
