from pathlib import Path
import json
import sys
import re
import socket as _sock_probe

from flask import Flask, Response, jsonify, request, send_from_directory, stream_with_context
from flask_cors import CORS


PROJECT_ROOT = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[1]
# Docker always builds the current frontend into ``frontend/dist``.  Prefer it
# over the repository's checked-in ``dist`` directory, which can be from an
# older release and otherwise makes a successful deployment serve stale UI.
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist" if (PROJECT_ROOT / "frontend" / "dist").is_dir() else (PROJECT_ROOT / "dist")
RELEASES_DIR = PROJECT_ROOT / "releases"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from modules.web_security.pentest import run_web_pentest
from modules.web_security.domain_scanner import analyze_domain
from modules.network_security.speed_checker import test_network_connection
from modules.web_security.scanner_hub import run_local_scanner, scanner_status
from modules.password_security import checker
from modules.network_security import checker as network_checker
from modules.network_security.device_scanner import nmap_profile_status, run_nmap_profile
from modules.phishing.url_analyzer import PhishingAnalyzer
from modules.phishing.threat_intel import ThreatIntelChecker as _ThreatIntelChecker
_threat_intel = _ThreatIntelChecker()
from modules.cryptography import crypto_tools
from modules.reports.report_exporter import REPORTS_DIRECTORY
from modules.reports.history import get_activity_history, record_activity


app = Flask(__name__)
CORS(app)


def _can_do_outbound_tcp() -> bool:
    """Quick probe: can this server open a real outbound TCP socket?
    Render free-tier blocks outbound raw sockets so the port scanner
    returns 0 results.  Detecting this early gives the user an honest
    message instead of a misleading empty table.
    """
    try:
        s = _sock_probe.socket(_sock_probe.AF_INET, _sock_probe.SOCK_STREAM)
        s.settimeout(0.8)
        s.connect(("1.1.1.1", 80))
        s.close()
        return True
    except Exception:
        return False



def remember_activity(module, target, status, summary, output=None):
    """History must never stop a completed security check from being returned."""
    try:
        record_activity(module, target, status, summary, output)
    except OSError as error:
        print(f"[!] Could not save activity history: {error}")


from modules.phishing.message_classifier import analyze_scam_message_advanced


def analyze_scam_message(text_content):
    """Return an explainable, multi-signal heuristic assessment of pasted scam text.

    Uses 500+ open-source indicators, OpenPhish/URLhaus feed intelligence,
    and contextual false-positive suppression.
    """
    return analyze_scam_message_advanced(text_content)



@app.get("/api/status")
def api_status():

    return jsonify({
        "success": True,
        "tool": "NIGHT HUNTER",
        "status": "online",
        "version": "1.6.2"
    })

@app.get("/api/version")
def api_version():
    return jsonify({
        "success": True,
        "version": "1.6.2",
        "release_url": "https://night-hunter-0br7.onrender.com/#downloads"
    })


@app.post("/api/web-security")
def web_security():

    try:

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "error": "Request body is missing."
            }), 400

        target = str(
            data.get("target", "")
        ).strip()

        if not target:

            return jsonify({
                "success": False,
                "error": "Target URL is required."
            }), 400

        # Operator-initiated scan is implicitly authorized
        authorized = data.get("authorized", True)

        if not target.startswith(
            ("http://", "https://")
        ):

            target = "https://" + target

        print()
        print("=" * 60)
        print("NIGHT HUNTER API - WEB SECURITY")
        print("=" * 60)
        print(f"Target: {target}")
        print()

        report = analyze_domain(target)
        remember_activity(
            "Web Security", target, "Complete",
            f"Completed domain intelligence scan for {report.get('recon', {}).get('hostname', target)}.",
            report,
        )

        return jsonify({
            "success": True,
            "target": target,
            "report": report
        })

    except Exception as error:

        print()
        print("[!] Web Security API error:")
        print(error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.get("/api/web-security/scanners")
def web_security_scanners():
    """Return real integration availability for the current device."""
    return jsonify({"success": True, **scanner_status()})


@app.post("/api/web-security/scanners/<scanner>")
def web_security_external_scanner(scanner):
    """Launch an explicitly selected, installed local scanner after consent."""
    data = request.get_json(silent=True) or {}
    authorized = data.get("authorized", True)
    target = str(data.get("target", "")).strip()
    if not target:
        return jsonify({"success": False, "error": "Target URL is required."}), 400
    try:
        result = run_local_scanner(scanner.lower(), target)
        remember_activity(
            "Web Security", target, "Complete",
            f"Completed local {scanner.lower()} scan.", result,
        )
        return jsonify({"success": True, "result": result})
    except (RuntimeError, ValueError) as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500


@app.post("/api/password-security")
def password_security():

    try:

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "error": "Request body is missing."
            }), 400

        password = str(
            data.get("password", "")
        )

        if not password:

            return jsonify({
                "success": False,
                "error": "Password is required."
            }), 400

        print()
        print("=" * 60)
        print("NIGHT HUNTER API - PASSWORD SECURITY")
        print("=" * 60)
        print("Password analysis started.")
        print()

        # Never print or store the actual password.
        analysis = checker.analyze_password(
            password
        )
        remember_activity(
            "Password Security", "Password input", "Complete",
            f"Password strength: {analysis.get('rating', 'analysed')}", analysis,
        )

        return jsonify({
            "success": True,
            "analysis": analysis
        })

    except Exception as error:

        print()
        print("[!] Password Security API error:")
        print(error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.post("/api/network-security")
def network_security():

    try:

        data = request.get_json(silent=True) or {}
        target = str(data.get("target", "")).strip()

        if not target:
            return jsonify({
                "success": False,
                "error": "Target IP address or hostname is required to initiate scan."
            }), 400

        print()
        print("=" * 60)
        print("NIGHT HUNTER API - NETWORK RECONNAISSANCE")
        print("=" * 60)
        print(f"Target: {target}")
        print()

        # Detect cloud / sandbox environments where outbound raw TCP
        # is blocked (Render free tier, GitHub Actions, etc.).
        if not _can_do_outbound_tcp():
            print("[!] Outbound TCP blocked - cloud environment detected")
            return jsonify({
                "success": False,
                "cloud_limitation": True,
                "error": (
                    "Port scanning requires direct network access. "
                    "This cloud server cannot open raw TCP sockets to external hosts. "
                    "Run Night Hunter locally for full port scan functionality."
                )
            }), 503

        result = test_network_connection(target)
        if not result.get("success"):
            return jsonify(result), 400

        total_open = result.get("total_open_ports", 0)
        posture_grade = result.get("security_posture", {}).get("posture_grade", "Scanned")
        remember_activity(
            "Network Recon", target, "Complete",
            f"Network socket recon for {target}: {total_open} open ports ({posture_grade}).",
            result,
        )

        return jsonify({
            "success": True,
            "target": target,
            "result": result
        })

    except Exception as error:

        print()
        print("[!] Network Security API error:")
        print(error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.post("/api/network-security/stream")
def network_security_stream():
    """Stream each advanced network-check result to the local dashboard."""
    data = request.get_json(silent=True) or {}
    target = str(data.get("target", "")).strip()

    if not target:
        return jsonify({
            "success": False,
            "error": "Target host or IP is required."
        }), 400

    def generate():
        for update in network_checker.iter_network_check(target):
            if update.get("type") == "complete":
                result = update.get("result", {})
                if result.get("success"):
                    remember_activity(
                        "Network Security", target, "Complete",
                        f"Completed authorized network inspection; {result.get('total_open_ports', 0)} open port(s) found.",
                        result,
                    )
            yield f"data: {json.dumps(update)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/network-security/nmap/status")
def network_nmap_status():
    return jsonify({"success": True, "nmap": nmap_profile_status()})


@app.post("/api/network-security/nmap")
def network_nmap_scan():
    data = request.get_json(silent=True) or {}
    target = str(data.get("target", "")).strip()
    profile = str(data.get("profile", "inventory")).strip()
    result = run_nmap_profile(target, profile)
    if not result.get("success"):
        return jsonify(result), 400
    remember_activity("Network Security", target, "Complete", f"Completed local Nmap {profile} profile.", result)
    return jsonify(result)


@app.post("/api/phishing")
def phishing_analysis():
    """Analyze URL characteristics without fetching remote page, with email/text triage and homoglyphs."""
    try:
        data = request.get_json(silent=True) or {}
        target = str(data.get("target", "")).strip()
        mode = str(data.get("mode", "url")).strip()
        text_content = str(data.get("text", "")).strip()
        if mode in {"email_triage", "message_triage", "sms_triage"} or (not target and text_content):
            if not text_content:
                return jsonify({"success": False, "error": "Paste a message, email, or SMS to analyse."}), 400
            result = analyze_scam_message(text_content)
            remember_activity(
                "Phishing Analyzer", f"Message triage ({result['total_links']} link(s))", "Complete",
                f"Local scam triage: {result['risk_level']} risk; {len(result['scam_patterns'])} signal group(s).", result,
            )
            return jsonify({"success": True, "report": result})

        if not target:
            return jsonify({"success": False, "error": "A URL is required."}), 400

        # 1. Offline brand/typosquatting check (instant, no network needed)
        report = PhishingAnalyzer(target, fetch_content=False).analyze()

        # 2. Real-time Threat Intelligence (VirusTotal, Google Safe Browsing, PhishTank, URLhaus)
        #    Fails gracefully if APIs are unavailable or keys not configured.
        try:
            from urllib.parse import urlsplit as _urlsplit
            _hostname = _urlsplit(target if "://" in target else "https://" + target).netloc or target
            ti = _threat_intel.check(target, hostname=_hostname)
            if isinstance(report, dict):
                # Merge threat intel findings
                existing = report.get("findings", [])
                existing.extend(ti.get("findings", []))
                report["findings"] = existing
                # Boost score if threat intel detected something
                ti_score = ti.get("threat_intel_score", 0)
                if ti_score > 0:
                    report["risk_score"] = min(100, max(report.get("risk_score", 0), ti_score))
                    if ti.get("threat_intel_verdict") == "MALICIOUS":
                        report["risk_level"] = "CRITICAL"
                    elif ti.get("threat_intel_verdict") == "SUSPICIOUS" and report.get("risk_level") in ("LOW", "MINIMAL", "BENIGN / VERIFIED"):
                        report["risk_level"] = "HIGH"
                report["threat_intelligence"] = {
                    "verdict": ti.get("threat_intel_verdict", "UNAVAILABLE"),
                    "flagged_by": ti.get("threat_intel_sources", []),
                    "api_keys_configured": ti.get("api_keys_configured", {}),
                    "details": ti.get("details", {})
                }
        except Exception:
            if isinstance(report, dict):
                report["threat_intelligence"] = {"verdict": "UNAVAILABLE", "flagged_by": [], "api_keys_configured": {}}

        risk = report.get("risk_level", report.get("risk", "Analysed")) if isinstance(report, dict) else "Analysed"
        remember_activity(
            "Phishing Analyzer", target, "Complete",
            f"URL analysis with threat intelligence complete. Risk: {risk}.", report,
        )
        return jsonify({"success": True, "report": report})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.post("/api/cryptography")
def cryptography():
    try:
        data = request.get_json(silent=True) or {}
        operation = str(data.get("operation", "hash")).strip().lower()
        text = data.get("text")

        if operation == "generate_keys":
            result = crypto_tools.generate_security_keys()
            remember_activity(
                "Crypto Lab", "CSPRNG Key Generation", "Complete",
                "Generated secure random cryptographic tokens and keys.",
                {"operation": operation, "result": result},
            )
            return jsonify({"success": True, "operation": operation, "result": result})

        if text is None or text == "":
            return jsonify({"success": False, "error": "Text is required."}), 400

        operations = {
            "hash": lambda: crypto_tools.hash_text_all(text),
            "identify": lambda: crypto_tools.get_hash_information(text),
            "base64_encode": lambda: crypto_tools.base64_encode(text),
            "base64_decode": lambda: crypto_tools.base64_decode(text),
            "base32_encode": lambda: crypto_tools.base32_encode(text),
            "base32_decode": lambda: crypto_tools.base32_decode(text),
            "hex_encode": lambda: crypto_tools.hex_encode(text),
            "hex_decode": lambda: crypto_tools.hex_decode(text),
            "binary_encode": lambda: crypto_tools.binary_encode(text),
            "binary_decode": lambda: crypto_tools.binary_decode(text),
            "url_encode": lambda: crypto_tools.url_encode(text),
            "url_decode": lambda: crypto_tools.url_decode(text),
            "rot13": lambda: crypto_tools.rot13(text),
            "caesar_encrypt": lambda: crypto_tools.caesar_encrypt(text, data.get("shift", 3)),
            "caesar_decrypt": lambda: crypto_tools.caesar_decrypt(text, data.get("shift", 3)),
            "jwt_inspect": lambda: crypto_tools.inspect_jwt(text),
            "hmac_sha256": lambda: crypto_tools.hmac_digest(text, data.get("key", "night_hunter_secret"), "sha256"),
            "hmac_sha512": lambda: crypto_tools.hmac_digest(text, data.get("key", "night_hunter_secret"), "sha512"),
        }
        if operation not in operations:
            return jsonify({"success": False, "error": "Unsupported operation."}), 400

        result = operations[operation]()
        remember_activity(
            "Crypto Lab", "Local input", "Complete",
            f"Completed {operation.replace('_', ' ')} operation.",
            {"operation": operation, "result": result},
        )
        return jsonify({
            "success": True,
            "operation": operation,
            "result": result,
        })
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.get("/api/reports")
def reports():
    files = []
    for path in sorted(REPORTS_DIRECTORY.glob("night_hunter_*"), key=lambda item: item.stat().st_mtime, reverse=True):
        if path.is_file() and path.suffix.lower() in {".json", ".txt", ".html"}:
            files.append({
                "name": path.name,
                "format": path.suffix[1:].upper(),
                "size": path.stat().st_size,
                "modified": path.stat().st_mtime,
            })
    return jsonify({"success": True, "reports": files})


@app.get("/api/history")
def activity_history():
    """Dashboard activity, saved locally after each completed module action."""
    return jsonify({"success": True, "history": get_activity_history()})


@app.get("/downloads/<path:filename>")
def download_release(filename):
    """Direct download for release packages or cloud runtime instructions."""
    if RELEASES_DIR.is_dir() and (RELEASES_DIR / filename).is_file():
        return send_from_directory(RELEASES_DIR, filename, as_attachment=True)
    return jsonify({
        "success": False,
        "error": f"Release file '{filename}' is not available on this server.",
        "github_url": "https://github.com/ArnabHalder-CS/Night-Hunter"
    }), 404


@app.get("/")
@app.get("/<path:path>")
def frontend(path=""):
    """Serve the production React dashboard from the same local server."""
    requested_file = FRONTEND_DIST / path

    if path and requested_file.is_file():
        return send_from_directory(FRONTEND_DIST, path)

    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        NIGHT HUNTER API SERVER")
    print("=" * 60)
    print()

    print("[+] API server starting...")
    print()

    print("[+] Web Security endpoint:")
    print("    POST /api/web-security")
    print()

    print("[+] Password Security endpoint:")
    print("    POST /api/password-security")
    print()

    print("[+] Network Security endpoint:")
    print("    POST /api/network-security")
    print()

    print("[+] Health endpoint:")
    print("    GET  /api/status")
    print()

    print("[+] Local server:")
    print("    http://127.0.0.1:5000")
    print()

    print("[*] Press CTRL+C to stop.")
    print("=" * 60)
    print()

    app.run(host="127.0.0.1", port=5000, debug=False)
