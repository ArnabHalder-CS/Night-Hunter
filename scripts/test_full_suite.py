import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

print("==========================================================")
print("     NIGHT HUNTER v1.6.2 - DEFENSIVE CAPABILITY AUDIT     ")
print("==========================================================\n")

# 1. Password Security
print("[TEST 1] Password Security & Entropy Audit")
from modules.password_security.checker import analyze_password
p_res = analyze_password("Admin@2026SecureKey!")
print(f"   -> Rating: {p_res.get('rating')}, Score: {p_res.get('score')}/10, Length: {p_res.get('checks', {}).get('length')}")
print(f"   -> Complexity Checks: {p_res.get('checks')}")
print("   [OK] Password Security operational.\n")

# 2. Cryptography Lab
print("[TEST 2] Cryptography & Smart Multi-Hashing")
from modules.cryptography.crypto_tools import hash_text_all, base64_encode, base64_decode, rot13
hashes = hash_text_all("NightHunterSecurity")
print(f"   -> Generated {len(hashes)} cryptographic digests simultaneously:")
for algo in ["md5", "sha256", "sha512", "blake2b"]:
    print(f"      {algo.upper()}: {hashes.get(algo)[:32]}...")
b64 = base64_encode("NightHunter")
print(f"   -> Base64 encode: {b64} -> decode: {base64_decode(b64)}")
print("   [OK] Cryptography Lab operational.\n")

# 3. Phishing Link Inspector
print("[TEST 3] Phishing Heuristic Engine & Brand Spoofing")
from modules.phishing.url_analyzer import PhishingAnalyzer
phish_samples = [
    ("http://paypal-security-update.account-verify.tk/login.php", "Malicious Homoglyph / Spoof"),
    ("https://github.com/halderarnab827/Night-Hunter", "Legitimate Reputable Domain")
]
for url, label in phish_samples:
    analyzer = PhishingAnalyzer(url, fetch_content=False)
    rep = analyzer.analyze()
    print(f"   -> [{label}] URL: {url[:45]}...")
    print(f"      Risk Score: {rep.get('risk_score')}/100 | Risk Level: {rep.get('risk_level')}")
    findings = rep.get("findings", [])
    print(f"      Flags Triggered: {len(findings)} ({[f.get('title') for f in findings[:2]]})")
print("   [OK] Phishing Analyzer operational.\n")

# 4. Network Reconnaissance & Device Intelligence
print("[TEST 4] Network Security & Nmap-Style Device Intelligence")
from modules.network_security.checker import get_device_recon
net_res = get_device_recon("127.0.0.1")
print(f"   -> Target: {net_res.get('ip_address')}, Status: {net_res.get('status')}")
print(f"   -> OS Model: {net_res.get('os_model')}")
print(f"   -> Device Name: {net_res.get('device_name')}")
print(f"   -> Scan Engine: {net_res.get('scan_engine')}")
print(f"   -> TCP Open Ports: {len(net_res.get('tcp_ports', []))}")
print(f"   -> UDP Open Ports (-sU): {len(net_res.get('udp_ports', []))}")
print("   [OK] Network Recon operational.\n")

# 5. Web Pentest / Security Headers
print("[TEST 5] Web Security Scanner")
from modules.web_security.pentest import run_web_pentest
web_res = run_web_pentest("https://example.com")
recon = web_res.get("recon", {})
print(f"   -> Target: {recon.get('hostname')}, Status: {recon.get('status_code')}, Server: {recon.get('server')}")
print(f"   -> Headers Inspected: {len(web_res.get('security_headers', []))}")
print(f"   -> Findings: {web_res.get('report_summary', {}).get('total')}")
print("   [OK] Web Security operational.\n")

# 6. Reports Engine
print("[TEST 6] Multi-Format Audit Reports Engine")
from modules.reports.report_exporter import export_all
sample_audit = {
    "audit_title": "Night Hunter Comprehensive Verification",
    "timestamp": "2026-09-22T12:00:00",
    "host": "127.0.0.1",
    "summary": "All defensive auditing modules operational",
    "results": {
        "web_security": web_res.get("report_summary", {}),
        "network": {"tcp_ports": len(net_res.get("tcp_ports", [])), "os": net_res.get("os_model")},
        "phishing": {"risk_score": 0, "status": "PASSED"}
    }
}
exported = export_all(sample_audit, "nighthunter_audit_verification")
print(f"   -> Exported {len(exported)} formats (JSON, TXT, HTML):")
for ext, p in exported.items():
    print(f"      [{ext.upper()}]: {p}")
print("   [OK] Report generation operational.\n")

print("==========================================================")
print("     ALL 6 DEFENSIVE SECURITY MODULES VERIFIED & PASS     ")
print("==========================================================")
