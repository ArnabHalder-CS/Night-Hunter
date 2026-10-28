#!/usr/bin/env python3
# ============================================================
# NIGHT HUNTER — Threat Intelligence API Layer
# ============================================================
# Checks unknown domains against real-time threat intelligence:
#   - VirusTotal (70+ AV engines)
#   - Google Safe Browsing
#   - PhishTank (crowdsourced phishing DB)
#   - URLhaus (abuse.ch malware/botnet URLs)
#
# USAGE:
#   from modules.phishing.threat_intel import ThreatIntelChecker
#   checker = ThreatIntelChecker()
#   result = checker.check(url)   # -> dict
#
# API KEYS: Set as environment variables (optional — graceful fallback)
#   VIRUSTOTAL_API_KEY       → get free at https://www.virustotal.com/gui/join-us
#   GOOGLE_SAFE_BROWSING_KEY → get free at https://developers.google.com/safe-browsing
# ============================================================

import os
import json
import base64
import hashlib
import socket
import time
from urllib.parse import urlsplit
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

VIRUSTOTAL_API_KEY      = os.environ.get("VIRUSTOTAL_API_KEY", "")
GOOGLE_SAFE_BROWSING_KEY = os.environ.get("GOOGLE_SAFE_BROWSING_KEY", "")

_API_TIMEOUT = 8  # seconds per request


# ── Helpers ──────────────────────────────────────────────────────────────────

def _http_post(url: str, payload: dict, headers: dict = None, timeout: int = _API_TIMEOUT) -> dict:
    """Simple urllib POST — no external dependencies."""
    body = json.dumps(payload).encode("utf-8")
    h = {"Content-Type": "application/json", "User-Agent": "NightHunter/3.0"}
    if headers:
        h.update(headers)
    req = Request(url, data=body, headers=h, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError, Exception):
        return {}


def _http_get(url: str, headers: dict = None, timeout: int = _API_TIMEOUT) -> dict:
    """Simple urllib GET — no external dependencies."""
    h = {"User-Agent": "NightHunter/3.0"}
    if headers:
        h.update(headers)
    req = Request(url, headers=h)
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError, Exception):
        return {}


# ── VirusTotal ───────────────────────────────────────────────────────────────

def check_virustotal(url: str) -> dict:
    """
    Check URL against VirusTotal using their v3 API.
    Free tier: 4 requests/minute, 500/day.
    Get key at https://www.virustotal.com/gui/join-us
    Returns: {"available": bool, "malicious": int, "suspicious": int,
              "total_engines": int, "verdict": str, "permalink": str}
    """
    if not VIRUSTOTAL_API_KEY:
        return {"available": False, "reason": "No VIRUSTOTAL_API_KEY set"}

    # VT v3 uses base64url-encoded URL as ID
    url_id = base64.urlsafe_b64encode(url.encode()).rstrip(b"=").decode()
    api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    data = _http_get(api_url, headers={"x-apikey": VIRUSTOTAL_API_KEY})

    if not data or "data" not in data:
        # URL not yet in VT — submit it
        submit_url = "https://www.virustotal.com/api/v3/urls"
        body = f"url={url}".encode()
        req = Request(submit_url, data=body,
                      headers={"x-apikey": VIRUSTOTAL_API_KEY,
                               "Content-Type": "application/x-www-form-urlencoded",
                               "User-Agent": "NightHunter/3.0"},
                      method="POST")
        try:
            from urllib.request import urlopen
            with urlopen(req, timeout=_API_TIMEOUT) as resp:
                submit_data = json.loads(resp.read().decode("utf-8"))
            # Try getting the analysis result
            analysis_id = submit_data.get("data", {}).get("id", "")
            if analysis_id:
                time.sleep(3)  # wait for scan
                analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                data = _http_get(analysis_url, headers={"x-apikey": VIRUSTOTAL_API_KEY})
                stats = data.get("data", {}).get("attributes", {}).get("stats", {})
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                total = sum(stats.values()) if stats else 0
                verdict = "MALICIOUS" if malicious > 0 else ("SUSPICIOUS" if suspicious > 0 else "CLEAN")
                return {
                    "available": True,
                    "malicious": malicious,
                    "suspicious": suspicious,
                    "total_engines": total,
                    "verdict": verdict,
                    "permalink": f"https://www.virustotal.com/gui/url/{url_id}"
                }
        except Exception:
            return {"available": False, "reason": "VirusTotal submission failed"}
        return {"available": False, "reason": "URL not yet in VirusTotal database"}

    attrs = data.get("data", {}).get("attributes", {})
    last_analysis = attrs.get("last_analysis_stats", {})
    malicious   = last_analysis.get("malicious", 0)
    suspicious  = last_analysis.get("suspicious", 0)
    total       = sum(last_analysis.values()) if last_analysis else 0
    verdict     = "MALICIOUS" if malicious > 0 else ("SUSPICIOUS" if suspicious > 0 else "CLEAN")

    return {
        "available": True,
        "malicious": malicious,
        "suspicious": suspicious,
        "total_engines": total,
        "verdict": verdict,
        "permalink": f"https://www.virustotal.com/gui/url/{url_id}",
        "categories": list(attrs.get("categories", {}).values())[:3],
    }


# ── Google Safe Browsing ──────────────────────────────────────────────────────

def check_google_safe_browsing(url: str) -> dict:
    """
    Check URL against Google's Safe Browsing API v4.
    Free: 10,000 requests/day.
    Get key at https://developers.google.com/safe-browsing/v4/get-started
    Returns: {"available": bool, "is_threat": bool, "threat_types": list}
    """
    if not GOOGLE_SAFE_BROWSING_KEY:
        return {"available": False, "reason": "No GOOGLE_SAFE_BROWSING_KEY set"}

    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_KEY}"
    payload = {
        "client": {"clientId": "night-hunter", "clientVersion": "3.0.0"},
        "threatInfo": {
            "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                 "POTENTIALLY_HARMFUL_APPLICATION", "THREAT_TYPE_UNSPECIFIED"],
            "platformTypes":    ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries":    [{"url": url}]
        }
    }

    data = _http_post(api_url, payload)
    matches = data.get("matches", [])
    threat_types = list({m.get("threatType", "") for m in matches if m.get("threatType")})

    return {
        "available": True,
        "is_threat": len(matches) > 0,
        "threat_types": threat_types,
        "verdict": "MALICIOUS" if matches else "CLEAN"
    }


# ── PhishTank ────────────────────────────────────────────────────────────────

def check_phishtank(url: str) -> dict:
    """
    Check URL against PhishTank crowdsourced phishing database.
    Free, no API key needed (anonymous access, rate limited).
    Returns: {"available": bool, "is_phishing": bool, "verified": bool}
    """
    from urllib.parse import urlencode
    api_url = "https://checkurl.phishtank.com/checkurl/"
    body = urlencode({
        "url": base64.b64encode(url.encode()).decode(),
        "format": "json",
        "app_key": ""
    }).encode()
    req = Request(api_url, data=body,
                  headers={"User-Agent": "phishtank/NightHunter",
                           "Content-Type": "application/x-www-form-urlencoded"},
                  method="POST")
    try:
        from urllib.request import urlopen
        with urlopen(req, timeout=_API_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        result = data.get("results", {})
        return {
            "available": True,
            "is_phishing": result.get("in_database", False) and result.get("valid", False),
            "verified": result.get("verified", False),
            "verdict": "MALICIOUS" if (result.get("in_database") and result.get("valid")) else "UNKNOWN"
        }
    except Exception:
        return {"available": False, "reason": "PhishTank request failed"}


# ── URLhaus ───────────────────────────────────────────────────────────────────

def check_urlhaus(url: str) -> dict:
    """
    Check URL against URLhaus (abuse.ch) malware URL database.
    Free, no API key needed.
    Returns: {"available": bool, "is_malicious": bool, "threat": str, "tags": list}
    """
    from urllib.parse import urlencode
    api_url = "https://urlhaus-api.abuse.ch/v1/url/"
    body = urlencode({"url": url}).encode()
    req = Request(api_url, data=body,
                  headers={"User-Agent": "NightHunter/3.0",
                           "Content-Type": "application/x-www-form-urlencoded"},
                  method="POST")
    try:
        from urllib.request import urlopen
        with urlopen(req, timeout=_API_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        query_status = data.get("query_status", "")
        if query_status == "is_reporting_server":
            return {"available": True, "is_malicious": False, "verdict": "REPORTING_SERVER"}
        if query_status == "no_results":
            return {"available": True, "is_malicious": False, "verdict": "CLEAN"}
        threat = data.get("threat", "")
        tags   = data.get("tags", []) or []
        url_status = data.get("url_status", "")
        is_malicious = url_status in ("online", "offline") and query_status == "is_reporting_server" or (
            threat != "" or len(tags) > 0
        )
        return {
            "available": True,
            "is_malicious": is_malicious or url_status == "online",
            "threat": threat,
            "tags": tags,
            "url_status": url_status,
            "verdict": "MALICIOUS" if (is_malicious or url_status == "online") else "CLEAN"
        }
    except Exception:
        return {"available": False, "reason": "URLhaus request failed"}


# ── IP Reputation ─────────────────────────────────────────────────────────────

def check_ip_reputation(hostname: str) -> dict:
    """
    Resolve hostname to IP, then check:
    - Is it a hosting/VPS provider? (phishing sites often use cheap VPS)
    - Basic reverse DNS mismatch detection
    Returns: {"available": bool, "ip": str, "suspicious": bool, "reasons": list}
    """
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        return {"available": False, "reason": "Could not resolve hostname"}

    reasons = []
    suspicious = False

    # Check if IP resolves back to same hostname (reverse DNS mismatch = suspicious)
    try:
        rdns = socket.gethostbyaddr(ip)[0]
        if hostname.lower() not in rdns.lower() and rdns.lower() not in hostname.lower():
            reasons.append(f"Reverse DNS mismatch: IP {ip} resolves to '{rdns}', not '{hostname}'")
            suspicious = True
    except Exception:
        reasons.append(f"No reverse DNS record for IP {ip}")
        suspicious = True

    # Known cheap VPS/hosting IP ranges often used by phishers
    SUSPICIOUS_HOSTING_PREFIXES = [
        "185.220.", "194.165.", "45.142.", "91.108.", "77.83.",
        "185.100.", "185.159.", "195.123.", "46.21.", "89.185.",
    ]
    for prefix in SUSPICIOUS_HOSTING_PREFIXES:
        if ip.startswith(prefix):
            reasons.append(f"IP {ip} belongs to a hosting range frequently associated with phishing infrastructure")
            suspicious = True
            break

    return {
        "available": True,
        "ip": ip,
        "suspicious": suspicious,
        "reasons": reasons,
        "verdict": "SUSPICIOUS" if suspicious else "CLEAN"
    }


# ── Master Checker ────────────────────────────────────────────────────────────

class ThreatIntelChecker:
    """
    Orchestrates all threat intelligence lookups.
    Designed to run AFTER the offline brand/typosquatting check.
    Adds additional score boost and findings based on real-time data.
    """

    def check(self, url: str, hostname: str = None) -> dict:
        """
        Run all available threat intelligence checks.

        Returns:
        {
            "threat_intel_score": int,       # 0–100 bonus score
            "threat_intel_verdict": str,     # MALICIOUS / SUSPICIOUS / CLEAN / UNAVAILABLE
            "threat_intel_sources": list,    # which APIs flagged it
            "findings": list,                # structured findings to merge into main report
            "details": {                     # raw results per service
                "virustotal": {...},
                "google_safe_browsing": {...},
                "phishtank": {...},
                "urlhaus": {...},
                "ip_reputation": {...}
            }
        }
        """
        if not hostname:
            try:
                hostname = urlsplit(url if "://" in url else "https://" + url).netloc or url
            except Exception:
                hostname = url

        details = {}
        flagged_by = []
        score_boost = 0
        findings = []

        # 1. VirusTotal
        vt = check_virustotal(url)
        details["virustotal"] = vt
        if vt.get("available") and vt.get("verdict") == "MALICIOUS":
            engines = vt.get("malicious", 0)
            flagged_by.append(f"VirusTotal ({engines} engines)")
            score_boost = max(score_boost, 90)
            findings.append({
                "title": "VirusTotal Multi-Engine Threat Detection",
                "severity": "CRITICAL",
                "summary": f"Flagged as malicious by {engines} out of {vt.get('total_engines', 0)} security engines",
                "description": f"VirusTotal aggregates 70+ antivirus and URL scanners. {engines} engines independently classified this URL as malicious — indicating high confidence of active phishing or malware delivery.",
                "evidence": f"VT malicious={engines}, suspicious={vt.get('suspicious', 0)}, permalink={vt.get('permalink', '')}",
                "recommendation": "Block this URL at all network layers immediately. Report to your SOC.",
                "score": 90,
                "confidence": "HIGH",
                "mitre_technique": "T1566.002",
                "mitre_tactic": "Initial Access"
            })
        elif vt.get("available") and vt.get("verdict") == "SUSPICIOUS":
            flagged_by.append("VirusTotal (suspicious)")
            score_boost = max(score_boost, 50)

        # 2. Google Safe Browsing
        gsb = check_google_safe_browsing(url)
        details["google_safe_browsing"] = gsb
        if gsb.get("available") and gsb.get("is_threat"):
            threat_types = gsb.get("threat_types", [])
            flagged_by.append(f"Google Safe Browsing ({', '.join(threat_types)})")
            score_boost = max(score_boost, 95)
            findings.append({
                "title": "Google Safe Browsing — Active Threat Confirmed",
                "severity": "CRITICAL",
                "summary": f"Listed in Google's real-time phishing/malware database: {', '.join(threat_types)}",
                "description": "Google Safe Browsing maintains real-time databases of malicious URLs. A match here means this URL is actively being used in phishing or malware campaigns and Google's products (Chrome, Gmail, Search) are already blocking it.",
                "evidence": f"Threat types: {threat_types}",
                "recommendation": "This URL is already blocked by major browsers. Do not visit. Report to CERT-In if targeting Indian users.",
                "score": 95,
                "confidence": "HIGH",
                "mitre_technique": "T1566.002",
                "mitre_tactic": "Initial Access"
            })

        # 3. PhishTank
        pt = check_phishtank(url)
        details["phishtank"] = pt
        if pt.get("available") and pt.get("is_phishing"):
            verified = "verified" if pt.get("verified") else "reported"
            flagged_by.append(f"PhishTank ({verified})")
            score_boost = max(score_boost, 85)
            findings.append({
                "title": "PhishTank — Confirmed Phishing URL",
                "severity": "CRITICAL",
                "summary": f"Listed in PhishTank crowdsourced phishing database ({verified})",
                "description": "PhishTank is a community-driven database of confirmed phishing URLs. This URL has been submitted and verified as a phishing site by multiple independent contributors.",
                "evidence": f"PhishTank status: {verified}",
                "recommendation": "Do not visit. Warn your users. Submit to your email gateway blocklist.",
                "score": 85,
                "confidence": "HIGH",
                "mitre_technique": "T1566.002",
                "mitre_tactic": "Initial Access"
            })

        # 4. URLhaus
        uh = check_urlhaus(url)
        details["urlhaus"] = uh
        if uh.get("available") and uh.get("is_malicious"):
            threat = uh.get("threat", "malware")
            tags = uh.get("tags", [])
            flagged_by.append(f"URLhaus ({threat})")
            score_boost = max(score_boost, 80)
            findings.append({
                "title": "URLhaus — Malware Distribution URL",
                "severity": "CRITICAL",
                "summary": f"Listed in URLhaus (abuse.ch) as active malware distribution point: {threat}",
                "description": f"URLhaus tracks malicious URLs used to distribute malware and malicious payloads. Tags: {tags}. This URL is actively serving malicious content.",
                "evidence": f"Threat: {threat}, Tags: {tags}, Status: {uh.get('url_status', 'unknown')}",
                "recommendation": "Block at firewall and email gateway. Do not download any content from this URL.",
                "score": 80,
                "confidence": "HIGH",
                "mitre_technique": "T1105",
                "mitre_tactic": "Command and Control"
            })

        # 5. IP reputation
        ip_rep = check_ip_reputation(hostname)
        details["ip_reputation"] = ip_rep
        if ip_rep.get("available") and ip_rep.get("suspicious"):
            reasons = ip_rep.get("reasons", [])
            flagged_by.append("IP Reputation Check")
            score_boost = max(score_boost, score_boost + 15)  # additive, not override
            findings.append({
                "title": "Suspicious Hosting Infrastructure",
                "severity": "HIGH",
                "summary": f"IP {ip_rep.get('ip', 'unknown')} shows suspicious hosting characteristics",
                "description": "The server hosting this domain shows indicators consistent with phishing infrastructure: " + "; ".join(reasons),
                "evidence": f"IP: {ip_rep.get('ip')}, Reasons: {reasons}",
                "recommendation": "Verify the domain ownership before interacting. Cross-reference IP with threat intelligence feeds.",
                "score": 30,
                "confidence": "MEDIUM",
                "mitre_technique": "T1583.003",
                "mitre_tactic": "Resource Development"
            })

        # Overall verdict
        if score_boost >= 80:
            verdict = "MALICIOUS"
        elif score_boost >= 40:
            verdict = "SUSPICIOUS"
        elif not any(d.get("available") for d in details.values()):
            verdict = "UNAVAILABLE"
        else:
            verdict = "CLEAN"

        return {
            "threat_intel_score": min(score_boost, 100),
            "threat_intel_verdict": verdict,
            "threat_intel_sources": flagged_by,
            "api_keys_configured": {
                "virustotal": bool(VIRUSTOTAL_API_KEY),
                "google_safe_browsing": bool(GOOGLE_SAFE_BROWSING_KEY),
            },
            "findings": findings,
            "details": details
        }


# ── Standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://malware.testing.google.test/testing/malware/"
    print(f"Checking: {url}")
    checker = ThreatIntelChecker()
    result = checker.check(url)
    print(json.dumps(result, indent=2))
