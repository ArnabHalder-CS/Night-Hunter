"""
modules/phishing/message_classifier.py
NIGHT HUNTER - Explainable Multi-Signal Scam & Smishing Analysis Engine

Integrates:
1. Threat intelligence keyword matching from data/scam_keywords.csv and SCAM_INTEL_CATEGORIES
2. Real-time local cache of known phishing domains (OpenPhish / URLhaus)
3. Specialized Indian cybercrime detection (KYC, electricity disconnection, digital arrest, UPI collect, task fraud)
4. Contextual combinations of signals (preventing false positives on harmless words like 'bank', 'verify', 'refund')
5. Calibration and explainability (Reasons, Excerpts, Confidence, Recommendations)
"""

import re
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
URLS_DIR = PROJECT_ROOT / "datasets" / "url_intelligence"

_THREAT_DOMAINS_CACHE = None
_SCAM_KEYWORDS_CACHE = None

def get_threat_domains():
    global _THREAT_DOMAINS_CACHE
    if _THREAT_DOMAINS_CACHE is not None:
        return _THREAT_DOMAINS_CACHE

    threat_file = URLS_DIR / "active_threat_urls.json"
    domains = set()
    if threat_file.is_file():
        try:
            with open(threat_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for d in data.get("openphish_domains", []):
                    domains.add(d.lower())
                for d in data.get("urlhaus_domains", []):
                    domains.add(d.lower())
        except Exception:
            pass
    _THREAT_DOMAINS_CACHE = domains
    return domains


def get_categorized_keywords():
    global _SCAM_KEYWORDS_CACHE
    if _SCAM_KEYWORDS_CACHE is not None:
        return _SCAM_KEYWORDS_CACHE

    # Load from scam_keywords.csv if present, and merge with SCAM_INTEL_CATEGORIES
    csv_path = DATA_DIR / "scam_keywords.csv"
    categories = {}
    if csv_path.is_file():
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cat = row.get("category", "General Phishing").strip()
                    kw = row.get("keyword_phrase", "").strip().lower()
                    sev = row.get("severity", "medium").strip().lower()
                    if not kw or len(kw) < 2:
                        continue
                    if cat not in categories:
                        categories[cat] = {
                            "base_weight": 14,
                            "bonus": 5,
                            "keywords": []
                        }
                    w_cand = 28 if sev == "critical" else 22 if sev == "high" else 14
                    if w_cand > categories[cat]["base_weight"]:
                        categories[cat]["base_weight"] = w_cand
                    categories[cat]["keywords"].append(kw)
        except Exception:
            categories = {}

    from modules.phishing.scam_intel import SCAM_INTEL_CATEGORIES
    for cat, meta in SCAM_INTEL_CATEGORIES.items():
        if cat not in categories:
            categories[cat] = {
                "base_weight": meta.get("base_weight", 20),
                "bonus": meta.get("bonus", 4),
                "keywords": list(meta.get("keywords", []))
            }
        else:
            # Merge any keywords in SCAM_INTEL_CATEGORIES that may not have been in CSV
            existing_set = set(categories[cat]["keywords"])
            for kw in meta.get("keywords", []):
                clean_kw = kw.strip().lower()
                if clean_kw not in existing_set:
                    categories[cat]["keywords"].append(clean_kw)
                    existing_set.add(clean_kw)

    _SCAM_KEYWORDS_CACHE = categories
    return categories


def analyze_scam_message_advanced(text_content):
    """
    Evaluates message text across 7 independent defensive layers:
    1. Keyword & phrase taxonomy (500+ patterns)
    2. Sensitive data harvesting (OTP, PIN, Card, Aadhaar, PAN)
    3. Urgency & Coercion triggers
    4. Threat URL intelligence (extracted links vs live feeds & IP/shorteners)
    5. Financial lures & multi-currency regexes
    6. Contextual combination logic (differentiating alerts vs scams)
    7. Explainable risk justification & actionable guidance
    """
    if not text_content or not text_content.strip():
        return {
            "mode": "message_triage",
            "risk_score": 0,
            "risk_level": "LOW",
            "confidence": "HIGH",
            "assessment_note": "No text provided. Paste a message or email body to evaluate.",
            "scam_patterns": [],
            "extracted_urls": [],
            "url_reports": [],
            "reasons": ["Empty message text."],
            "recommended_actions": ["Provide message content to start automated defensive analysis."],
            "total_links": 0,
            "high_risk_links": 0,
            "is_uncertain": False
        }

    raw_text = text_content.strip()
    normalized = re.sub(r"\s+", " ", raw_text.lower())
    # Attacker homoglyph / typo de-obfuscation commonly observed in SMS smishing
    normalized = normalized.replace("parcei", "parcel").replace("heid", "held").replace("piease", "please").replace("confrim", "confirm")
    categories_dict = get_categorized_keywords()
    threat_domains = get_threat_domains()

    patterns = []
    matched_categories = set()
    category_hits = 0
    raw_score = 0
    reasons = []

    # 1. CATEGORIZED KEYWORD MATCHING
    for category, meta in categories_dict.items():
        base_weight = meta.get("base_weight", 16)
        bonus_per_extra = meta.get("bonus", 4)
        phrases = meta.get("keywords", [])
        matched = []
        for phrase in phrases:
            # Word-boundary or substring check
            if phrase in normalized:
                matched.append(phrase)

        if matched:
            matched_categories.add(category)
            # Cap bonus at 4 distinct hits per category to avoid score explosion on repetitive text
            capped_extra = min(len(matched) - 1, 4)
            cat_score = base_weight + (bonus_per_extra * capped_extra)
            patterns.append({
                "category": category,
                "keywords": matched[:5],
                "weight": cat_score
            })
            raw_score += cat_score
            category_hits += 1

    # 2. URL EXTRACTION & THREAT-INTEL FEEDS
    # Support http://, https://, www., and common shorteners / path-based or bare domains
    url_pattern = re.compile(
        r"(?:https?://[^\s<>\"'()\[\]]+|"
        r"www\.[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+(?:/[^\s<>\"'()\[\]]*)?|"
        r"\b[a-zA-Z0-9-]+\.(?:com|org|net|info|biz|xyz|top|app|online|site|link|cc|ru|in|co|io|ly|vc|li|to|gl|click|work|buzz|club|live|shop|vip|me|mobi|fit|icu|cfd|sbs|rest|monster|3utilities\.com|hk-ssl\.net)(?:/[^\s<>\"'()\[\]]*)?"
        r")",
        re.IGNORECASE
    )
    raw_matches = url_pattern.finditer(raw_text)
    found_urls = []
    for m in raw_matches:
        u = m.group(0).strip(".,;:!?)]}\"'")
        if u.startswith("."):
            u = u[1:]
        if u and u not in found_urls:
            found_urls.append(u)

    url_findings = []
    malicious_feed_hits = 0

    SHORTENERS = {
        "bit.ly", "tinyurl.com", "t.co", "shorturl.at", "is.gd", "rb.gy", "cutt.ly",
        "tx.vc", "ko.gl", "cntr.click", "usnd.to", "drip.io", "twil.io", "kvo6.io",
        "ksub.io", "kuy8.com", "lybr.at", "surl.li"
    }
    SUSPICIOUS_DOMAINS = {
        "3utilities.com", "duckdns.org", "ddns.net", "ngrok-free.app", "serveo.net",
        "hk-ssl.net", "bplaced.net"
    }
    BRAND_KEYWORDS = [
        "sbi", "citi", "citbank", "boa", "bankofamerica", "westpac", "commbank", "cba",
        "anz", "usps", "indiapost", "ups", "fedex", "dhl", "amazon", "netflix", "paypal"
    ]
    ACTION_DOMAIN_WORDS = [
        "login", "verify", "update", "support", "service", "weblogin", "confirm", "secure",
        "officetrack", "track", "parcel", "delivery", "admin"
    ]

    has_threat_flag = False

    for u in found_urls[:10]:
        fixed_url = u if u.startswith("http") else f"https://{u}"
        parsed = urlparse(fixed_url)
        raw_host = parsed.netloc.lower() or parsed.path.lower().split("/")[0]
        domain = raw_host.split(":")[0]  # strip port
        findings_for_url = []

        # Check against OpenPhish & URLhaus live threat cache
        if domain in threat_domains:
            malicious_feed_hits += 1
            findings_for_url.append("Domain confirmed on open threat intelligence feeds (OpenPhish/URLhaus)")
            reasons.append(f"Contains link to active flagged domain: {domain}")
            has_threat_flag = True

        # Check IP-based URL - safely distinguish private/LAN vs public raw IP
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
            try:
                import ipaddress
                ip_obj = ipaddress.ip_address(domain)
                if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                    findings_for_url.append("Private/LAN IP address (local development or intranet)")
                else:
                    findings_for_url.append("Public numeric IP address used instead of domain name")
                    raw_score += 20
                    reasons.append(f"Public numeric IP link observed ({domain}); commonly seen in unindexed phishing hosts")
                    has_threat_flag = True
            except ValueError:
                pass

        # Check URL shortener
        if any(s in domain for s in SHORTENERS):
            findings_for_url.append("Obfuscated through URL shortener or redirector")
            raw_score += 18
            reasons.append(f"Shortened link masks destination host: {domain}")
            has_threat_flag = True

        # Check Free/Dynamic DNS
        if any(sd in domain for sd in SUSPICIOUS_DOMAINS):
            findings_for_url.append("Free dynamic DNS or abuse-prone hosting")
            raw_score += 25
            reasons.append(f"Uses dynamic DNS / unverified host: {domain}")
            has_threat_flag = True

        # Check Brand spoofing in domain
        has_brand = any(b in domain for b in BRAND_KEYWORDS)
        has_action = any(a in domain for a in ACTION_DOMAIN_WORDS)
        if has_brand and has_action:
            findings_for_url.append("Domain mimics recognized brand with action/login keywords")
            raw_score += 30
            reasons.append(f"Spoofed domain pattern targeting financial/postal service: {domain}")
            has_threat_flag = True
        elif has_action and any(cat in matched_categories for cat in ["Account Suspension & Security Threat", "Delivery, Customs & Package Phishing", "Credential or OTP harvesting"]):
            findings_for_url.append("Action-oriented destination domain linked to alert lure")
            raw_score += 20
            reasons.append(f"Destination domain matches message threat vector: {domain}")
            has_threat_flag = True

        # Check dangerous file extensions (.apk, .exe, .scr, .bat)
        if re.search(r"\.(?:apk|exe|bat|cmd|vbs|scr)$", parsed.path, re.I):
            findings_for_url.append("Points to executable binary or mobile application package (.apk/.exe)")
            if category_hits > 0 or any(w in normalized for w in ["install", "download", "track", "invoice", "update", "bill"]):
                raw_score += 30
                reasons.append("Direct package or executable download link in message context")
            else:
                raw_score += 15
            has_threat_flag = True

        url_findings.append({
            "url": u,
            "domain": domain,
            "flags": findings_for_url,
            "is_threat": len(findings_for_url) > 0
        })

    if malicious_feed_hits > 0:
        raw_score += (45 * malicious_feed_hits)

    # Unofficial link attached to Account Suspension, Delivery, Reward, or Loan alert
    if found_urls and not has_threat_flag:
        if any(cat in matched_categories for cat in ["Account Suspension & Security Threat", "Credential or OTP harvesting"]):
            raw_score += 25
            reasons.append("External unverified link provided to resolve account/security alert.")
        elif any(cat in matched_categories for cat in ["Delivery, Customs & Package Phishing", "Prize, Lottery, Bonus & Reward Lures", "Loan & Financial Fraud"]):
            raw_score += 20
            reasons.append("External link attached to delivery fee or reward lure.")

    # 3. MONETARY AMOUNTS & PRIZE CONTEXT
    # Only flag as scam signal if message ALSO contains prize, reward, refund, task, or urgency terms
    money_pattern = re.findall(
        r"(?:rs\.?|inr|₹|\$|usd|gbp|eur)\s*[\d,]+(?:\.\d+)?|[\d,]+(?:\.\d+)?\s*(?:rs\.?|inr|₹|rupees|dollars|lakhs?|crores?|thousand|million)",
        normalized
    )
    has_financial_lure = any(w in normalized for w in [
        "won", "winner", "prize", "lottery", "cashback", "reward", "selected",
        "refund", "unpaid", "claim", "deposit", "bonus", "part-time", "daily", "task"
    ])
    if money_pattern and has_financial_lure:
        patterns.append({
            "category": "Monetary lure identified",
            "keywords": [m.strip() for m in money_pattern[:3]],
            "weight": 12
        })
        raw_score += 12
        reasons.append(f"Monetary claim linked with promotional or pressure context: {', '.join(money_pattern[:2])}")

    # 4. FREEMAIL / FAKE CUSTOMER SUPPORT ADDRESS
    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw_text)
    freemails = [e for e in emails if re.search(r"@(?:gmail|yahoo|hotmail|outlook|proton|yandex)\.", e, re.I)]
    if freemails and category_hits > 0:
        patterns.append({
            "category": "Unofficial email contact",
            "keywords": freemails[:2],
            "weight": 14
        })
        raw_score += 14
        reasons.append("Official/banking claim provides generic public webmail address (Gmail/Yahoo/Hotmail)")

    # Phone numbers: only add weight if message has urgency/threat/coercion context
    has_coercion_or_threat = any(cat in matched_categories for cat in [
        "Urgency, Coercion & Pressure Tactics",
        "Account Suspension & Security Threat",
        "KYC, Identity & Utility Disconnection Scams",
        "Authority & Corporate Impersonation",
        "Electricity & utility disconnection"
    ])
    phone_pattern = re.findall(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)", raw_text)
    if phone_pattern and has_coercion_or_threat:
        raw_score += 10
        reasons.append("Contains contact phone number in high-pressure or coercive alert context")

    # 5. CONTEXTUAL FALSE-POSITIVE MITIGATION WITH SAFETY FLOOR
    has_otp_context = any(term in normalized for term in ["otp", "verification code", "one time password"])
    has_do_not_share = any(term in normalized for term in ["do not share", "never share", "not share with anyone", "strictly confidential", "bank never asks"])

    # Strong malicious indicators must NEVER be hidden by legitimate phrasing
    has_dangerous_file = any(u.get("flags") and any("binary" in str(f) or "executable" in str(f) for f in u.get("flags", [])) for u in url_findings)
    has_strong_malice = (
        malicious_feed_hits > 0
        or has_dangerous_file
        or any(cat in matched_categories for cat in ["Credential or OTP harvesting", "Sextortion & Blackmail Coercion"])
    )

    if not has_strong_malice:
        # If bank is warning the customer NEVER to share OTP, do NOT penalize as a scam
        if has_otp_context and has_do_not_share and len(found_urls) == 0:
            raw_score = max(0, raw_score - 40)
            reasons.append("Contains standard banking security advice ('do not share OTP') without external links.")

        # Legitimate banking transaction / credit alert
        is_transaction_alert = any(term in normalized for term in [
            "credited with", "debited with", "available balance", "neft", "imps", "rtgs", "clearing",
            "spent on", "spent on your", "card xx", "available limit", "spent at", "withdrawn from"
        ])
        has_no_links = (len(found_urls) == 0)
        has_no_action_demand = not any(term in normalized for term in ["click", "login", "call", "verify", "update", "share", "pay", "immediately", "block"])
        if is_transaction_alert and has_no_links and has_no_action_demand:
            raw_score = max(0, raw_score - 45)
            reasons.append("Standard bank transactional credit/debit notification with no action demand or links.")

        # Legitimate courier delivery notification
        is_courier_notice = any(term in normalized for term in ["out for delivery", "delivered today", "expected delivery", "shipped via", "arriving by"])
        if is_courier_notice and has_no_links and not any(w in normalized for w in ["fee", "pay", "customs", "held", "charge"]):
            raw_score = max(0, raw_score - 30)
            reasons.append("Standard courier status dispatch notification with no demands or unverified links.")

        # Single generic word penalty dampener
        if category_hits == 1 and raw_score < 25 and len(found_urls) == 0:
            raw_score = int(raw_score * 0.6)
            reasons.append("Only isolated generic keywords detected without malicious links or coercion.")

    # Compound vector boost: if message hits 2+ distinct threat categories
    if category_hits >= 2:
        raw_score = int(raw_score * 1.25)

    # If dangerous executable / APK is accompanied by social engineering lure, guarantee HIGH risk
    if has_dangerous_file and (category_hits > 0 or any(w in normalized for w in ["install", "download", "track", "invoice", "update", "bill"])):
        raw_score = max(raw_score, 65)

    # 6. SCORE CALIBRATION & RISK LEVEL
    score = min(max(raw_score, 0), 100)

    # Calibrated risk classification:
    # 60+ is HIGH risk (clear multi-signal or confirmed threat)
    # 35-59 is MEDIUM risk (suspicious patterns requiring caution)
    # <35 is LOW risk (benign/transactional or minimal indicators)
    if score >= 60 or malicious_feed_hits > 0:
        risk_level = "HIGH"
        confidence = "HIGH"
        if not reasons:
            reasons.append("Multiple high-severity social-engineering vectors detected.")
    elif score >= 35:
        risk_level = "MEDIUM"
        confidence = "MEDIUM"
        if not reasons:
            reasons.append("Suspicious phrasing and potential pressure tactics observed.")
    else:
        risk_level = "LOW"
        confidence = "HIGH" if score < 15 else "MEDIUM"
        if not reasons:
            reasons.append("No significant phishing patterns or malicious URLs detected.")

    # Uncertainty warning for borderline or mixed-signal cases
    is_uncertain = (35 <= score <= 55) or (category_hits >= 2 and len(found_urls) == 0 and has_do_not_share)

    # 7. TAILORED ACTIONABLE RECOMMENDATIONS
    actions = []
    if risk_level == "HIGH":
        actions.extend([
            "DO NOT click any links, open APKs/attachments, or respond to this message.",
            "DO NOT share OTPs, PINs, bank account numbers, or remote-access codes.",
            "If bank/government was impersonated, call the verified official helpline on the back of your card.",
            "Report scam messages to Cyber Crime portal (1930 in India / cybercrime.gov.in) or carrier spam filter."
        ])
    elif risk_level == "MEDIUM":
        actions.extend([
            "Exercise caution. Independently verify the message through the official app or website.",
            "Do not call phone numbers provided directly inside the message.",
            "Check the sender header/number to confirm authenticity."
        ])
    else:
        actions.extend([
            "Message appears relatively normal, but remain vigilant against unexpected requests.",
            "Always verify sender identity before making any payment or sharing personal information."
        ])

    return {
        "mode": "message_triage",
        "risk_score": score,
        "risk_level": risk_level,
        "confidence": confidence,
        "assessment_note": (
            "Heuristic threat estimate based on 500+ open-source indicators and real-time threat intelligence. "
            "A high score flags strong deceptive signals; always verify through independent channels."
        ),
        "scam_patterns": patterns,
        "urgency_triggers": patterns,  # Backward compatibility for existing frontends
        "extracted_urls": found_urls,
        "url_reports": url_findings,
        "total_links": len(found_urls),
        "high_risk_links": malicious_feed_hits + sum(1 for u in url_findings if u.get("is_threat")),
        "reasons": reasons,
        "recommended_actions": actions,
        "is_uncertain": is_uncertain,
        "matched_categories": list(matched_categories)
    }
