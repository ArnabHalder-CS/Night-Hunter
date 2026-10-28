# ============================================================
# NIGHT HUNTER
# ADVANCED PHISHING ANALYZER
# SINGLE FILE ENGINE
# ============================================================

import sys
import re
import json
import math
import time
import socket
import ssl
import ipaddress
import hashlib
import base64
import binascii
import unicodedata
import argparse

from datetime import datetime
from urllib.parse import (
    urlsplit,
    urlunsplit,
    urljoin,
    unquote,
    quote,
    parse_qsl
)

try:
    import requests
except ImportError:
    requests = None


# ============================================================
# VERSION
# ============================================================

TOOL_NAME = "NIGHT HUNTER"
MODULE_NAME = "Advanced Phishing Analyzer"
VERSION = "3.0.0"

DEFAULT_TIMEOUT = 10
MAX_REDIRECTS = 10
MAX_CONTENT_SIZE = 5 * 1024 * 1024


# ============================================================
# TERMINAL COLORS
# ============================================================

RESET = "\033[0m"

BLACK = "\033[30m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"

BOLD = "\033[1m"
DIM = "\033[2m"


# ============================================================
# SUSPICIOUS KEYWORDS
# ============================================================

SUSPICIOUS_KEYWORDS = {

    "login": 3,
    "log-in": 3,
    "signin": 3,
    "sign-in": 3,
    "verify": 4,
    "verification": 4,
    "validate": 3,
    "validation": 3,
    "confirm": 3,
    "confirmation": 3,
    "account": 2,
    "accounts": 2,
    "password": 4,
    "passwd": 4,
    "credential": 4,
    "credentials": 4,
    "security": 2,
    "secure": 2,
    "authentication": 3,
    "authenticate": 3,
    "auth": 2,
    "authorize": 3,
    "authorization": 3,
    "activate": 3,
    "activation": 3,
    "unlock": 3,
    "locked": 3,
    "suspended": 4,
    "suspension": 4,
    "reset": 3,
    "recover": 3,
    "recovery": 3,
    "billing": 3,
    "payment": 3,
    "payments": 3,
    "invoice": 2,
    "refund": 3,
    "wallet": 3,
    "bank": 3,
    "banking": 3,
    "support": 2,
    "customer": 1,
    "webmail": 3,
    "admin": 2,
    "administrator": 3,
    "urgent": 4,
    "urgency": 4,
    "immediately": 4,
    "important": 2,
    "alert": 3,
    "warning": 3,
    "limited": 2,
    "expire": 3,
    "expired": 3,
    "expiration": 3,
    "download": 2,
    "document": 1,
    "attachment": 2,
    "gift": 2,
    "bonus": 2,
    "reward": 2,
    "crypto": 2,
    "bitcoin": 2,
    "wallet": 3
}


# ============================================================
# SHORT URL SERVICES
# ============================================================

SHORTENER_DOMAINS = {

    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "rb.gy",
    "tiny.cc",
    "shorturl.at",
    "rebrand.ly",
    "surl.li",
    "v.gd",
    "lnkd.in",
    "amzn.to",
    "ift.tt",
    "soo.gd",
    "bl.ink",
    "shorte.st"

}


# ============================================================
# SUSPICIOUS TLDs
# ============================================================

SUSPICIOUS_TLDS = {

    "xyz",
    "top",
    "click",
    "link",
    "live",
    "online",
    "site",
    "shop",
    "icu",
    "buzz",
    "cam",
    "cyou",
    "monster",
    "work",
    "zip",
    "mov",
    "download",
    "loan",
    "rest",
    "tk",
    "pw",
    "gq",
    "ml",
    "cf",
    "ga"

}


# ============================================================
# COMMON BRANDS
# ============================================================

BRAND_NAMES = {

    "google",
    "gmail",
    "microsoft",
    "outlook",
    "office365",
    "office",
    "apple",
    "icloud",
    "amazon",
    "paypal",
    "facebook",
    "instagram",
    "linkedin",
    "netflix",
    "dropbox",
    "docusign",
    "adobe",
    "steam",
    "discord",
    "telegram",
    "whatsapp",
    "coinbase",
    "binance",
    "visa",
    "mastercard",
    "chase",
    "bankofamerica",
    "wellsfargo",
    "github",
    "gitlab",
    "spotify",
    "zoom",
    "salesforce",
    "twitter",
    "x"

}

# ============================================================
# OFFICIAL BRAND DOMAINS (WHITELIST & COMBO-SQUATTING MATRIX)
# ============================================================

OFFICIAL_BRAND_DOMAINS = {
    # ── Global Tech ──────────────────────────────────────────
    "google": {"google.com", "google.co.in", "google.co.uk", "google.ca", "google.de", "google.fr", "google.com.au", "gmail.com", "goo.gl", "gstatic.com"},
    "youtube": {"youtube.com", "youtu.be"},
    "reddit": {"reddit.com"},
    "tiktok": {"tiktok.com"},
    "ebay": {"ebay.com"},
    "yahoo": {"yahoo.com", "yahoo.co.in"},
    "twitch": {"twitch.tv"},
    "roblox": {"roblox.com"},
    "microsoft": {"microsoft.com", "live.com", "office.com", "office365.com", "outlook.com", "msn.com", "azure.com", "bing.com", "windows.com", "skype.com"},
    "apple": {"apple.com", "icloud.com", "itunes.com", "me.com"},
    "amazon": {"amazon.com", "amazon.co.uk", "amazon.de", "amazon.in", "amazon.ca", "amazon.fr", "primevideo.com"},
    "paypal": {"paypal.com", "paypal.me"},
    "netflix": {"netflix.com"},
    "meta": {"facebook.com", "instagram.com", "whatsapp.com", "meta.com", "fb.com"},
    "facebook": {"facebook.com", "fb.com"},
    "instagram": {"instagram.com"},
    "whatsapp": {"whatsapp.com", "wa.me"},
    "github": {"github.com", "github.io", "githubusercontent.com"},
    "dropbox": {"dropbox.com"},
    "adobe": {"adobe.com"},
    "docusign": {"docusign.com", "docusign.net"},
    "linkedin": {"linkedin.com"},
    "twitter": {"twitter.com", "x.com", "t.co"},
    "spotify": {"spotify.com"},
    "steam": {"steampowered.com", "steamcommunity.com"},
    "discord": {"discord.com", "discord.gg", "discordapp.com"},
    "telegram": {"telegram.org", "t.me"},
    "zoom": {"zoom.us", "zoom.com"},
    "salesforce": {"salesforce.com", "force.com"},
    "slack": {"slack.com"},
    # ── Crypto ───────────────────────────────────────────────
    "binance": {"binance.com", "binance.us"},
    "coinbase": {"coinbase.com"},
    "kraken": {"kraken.com"},
    # ── US Banking ───────────────────────────────────────────
    "chase": {"chase.com", "jpmorganchase.com", "jpmorgan.com"},
    "bankofamerica": {"bankofamerica.com", "bofa.com"},
    "wellsfargo": {"wellsfargo.com"},
    "citibank": {"citibank.com", "citi.com"},
    # ── Indian E-commerce ────────────────────────────────────
    "flipkart": {"flipkart.com"},
    "myntra": {"myntra.com"},
    "meesho": {"meesho.com"},
    "snapdeal": {"snapdeal.com"},
    "nykaa": {"nykaa.com"},
    "ajio": {"ajio.com"},
    "tatacliq": {"tatacliq.com"},
    "reliancedigital": {"reliancedigital.in"},
    # ── Indian Fintech / Payments ─────────────────────────────
    "paytm": {"paytm.com", "paytmbank.com"},
    "phonepe": {"phonepe.com"},
    "gpay": {"pay.google.com"},
    "razorpay": {"razorpay.com"},
    "mobikwik": {"mobikwik.com"},
    "freecharge": {"freecharge.in"},
    # ── Indian Banks ─────────────────────────────────────────
    "sbi": {"onlinesbi.sbi", "sbi.co.in", "onlinesbi.com"},
    "hdfc": {"hdfcbank.com", "hdfc.com"},
    "icici": {"icicibank.com"},
    "axis": {"axisbank.com"},
    "kotak": {"kotkamahindrabank.com", "kotak.com"},
    "pnb": {"pnbindia.in"},
    "unionbank": {"unionbankofindia.co.in"},
    "canara": {"canarabank.com"},
    # ── Indian Telecom ───────────────────────────────────────
    "jio": {"jio.com", "jiocinema.com", "jiomoney.com"},
    "airtel": {"airtel.in", "airtel.com", "airtelpay.in"},
    "vi": {"myvi.in", "vodafoneidea.com"},
    "bsnl": {"bsnl.co.in"},
    # ── Indian Food / Delivery ───────────────────────────────
    "swiggy": {"swiggy.com"},
    "zomato": {"zomato.com"},
    "dunzo": {"dunzo.in"},
    "blinkit": {"blinkit.com"},
    # ── Indian Travel ────────────────────────────────────────
    "irctc": {"irctc.co.in", "irctchelp.in"},
    "makemytrip": {"makemytrip.com"},
    "goibibo": {"goibibo.com"},
    "cleartrip": {"cleartrip.com"},
    "ixigo": {"ixigo.com"},
    # ── Indian OTT ───────────────────────────────────────────
    "hotstar": {"hotstar.com", "disneyplushotstar.com"},
    "sonyliv": {"sonyliv.com"},
    "zeespace": {"zee5.com"},
    # ── Other Indian Brands ───────────────────────────────────
    "ola": {"olacabs.com", "ola.com"},
    "uber": {"uber.com"},
    "rapido": {"rapido.bike"},
    "byju": {"byjus.com"},
    "zerodha": {"zerodha.com", "kite.zerodha.com"},
    "groww": {"groww.in"},
    "upstox": {"upstox.com"},
    "policybazaar": {"policybazaar.com"},
    "lenskart": {"lenskart.com"},
    "bigbasket": {"bigbasket.com"},
    "jiomart": {"jiomart.com"},
}

HIGH_RISK_PHISHING_TLDS = {
    "xyz", "top", "work", "click", "buzz", "club", "cam", "live", "loan", "vip", "icu",
    "gq", "cf", "ml", "tk", "ga", "rest", "country", "monster", "casa", "surf", "fit", "sbs", "cfd"
}

LEETSPEAK_MAP = {
    '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's',
    '7': 't', '8': 'b', '@': 'a', '$': 's', 'vv': 'w', 'rn': 'm'
}

def normalize_leetspeak(text):
    t = str(text or "").lower()
    for k, v in LEETSPEAK_MAP.items():
        t = t.replace(k, v)
    return t

def calculate_levenshtein(s1, s2):
    """Damerau-Levenshtein distance (handles transpositions).
    flipkart -> flipkert  = dist 1 (transposition a<->e)
    amazon   -> aamazon   = dist 1 (insertion)
    """
    s1, s2 = s1.lower(), s2.lower()
    len1, len2 = len(s1), len(s2)
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    # Full Damerau-Levenshtein with transposition support
    INF = len1 + len2 + 1
    # d[i][j] = edit distance between s1[:i] and s2[:j]
    d = [[INF] * (len2 + 2) for _ in range(len1 + 2)]
    d[0][0] = INF
    for i in range(len1 + 1):
        d[i + 1][0] = INF
        d[i + 1][1] = i
    for j in range(len2 + 1):
        d[0][j + 1] = INF
        d[1][j + 1] = j
    last_row = {}
    for i in range(1, len1 + 1):
        c1 = s1[i - 1]
        last_match_col = 0
        for j in range(1, len2 + 1):
            c2 = s2[j - 1]
            i2 = last_row.get(c2, 0)
            j2 = last_match_col
            cost = 0 if c1 == c2 else 1
            if c1 == c2:
                last_match_col = j
            d[i + 1][j + 1] = min(
                d[i][j] + cost,           # substitution / match
                d[i + 1][j] + 1,          # insertion
                d[i][j + 1] + 1,          # deletion
                d[i2][j2] + (i - i2 - 1) + 1 + (j - j2 - 1)  # transposition
            )
        last_row[c1] = i
    return d[len1 + 1][len2 + 1]



# ============================================================
# SUSPICIOUS FILE EXTENSIONS
# ============================================================

SUSPICIOUS_EXTENSIONS = {

    ".exe",
    ".scr",
    ".msi",
    ".bat",
    ".cmd",
    ".com",
    ".cpl",
    ".jar",
    ".ps1",
    ".vbs",
    ".vbe",
    ".js",
    ".jse",
    ".hta",
    ".apk",
    ".dmg",
    ".pkg",
    ".iso",
    ".img",
    ".zip",
    ".rar",
    ".7z",
    ".dll",
    ".bin"

}


# ============================================================
# REDIRECT PARAMETERS
# ============================================================

REDIRECT_PARAMETERS = {

    "url",
    "uri",
    "redirect",
    "redirect_url",
    "redirect_uri",
    "return",
    "returnurl",
    "return_url",
    "next",
    "continue",
    "destination",
    "dest",
    "target",
    "goto",
    "link",
    "to",
    "forward",
    "forward_url"

}


# ============================================================
# TRACKING PARAMETERS
# ============================================================

TRACKING_PARAMETERS = {

    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "fbclid",
    "gclid",
    "msclkid",
    "dclid",
    "mc_cid",
    "mc_eid"

}


# ============================================================
# SUSPICIOUS PORTS
# ============================================================

SUSPICIOUS_PORTS = {

    21,
    22,
    23,
    25,
    110,
    135,
    139,
    143,
    445,
    3389,
    5900,
    8080,
    8000,
    8008,
    8888,
    3000,
    5000,
    8001,
    9000

}


# ============================================================
# COMMON WEB PORTS
# ============================================================

COMMON_WEB_PORTS = {

    80,
    443,
    8080,
    8443

}


# ============================================================
# RESULT OBJECT
# ============================================================

class Finding:

    def __init__(
        self,
        category,
        severity,
        title,
        description,
        evidence="",
        recommendation="",
        score=0,
        confidence="MEDIUM"
    ):

        self.category = category
        self.severity = severity
        self.title = title
        self.description = description
        self.evidence = evidence
        self.recommendation = recommendation
        self.score = score
        self.confidence = confidence

        self.timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


    def to_dict(self):

        return {

            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "score": self.score,
            "confidence": self.confidence,
            "timestamp": self.timestamp

        }


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def safe_int(value, default=0):

    try:
        return int(value)

    except (TypeError, ValueError):

        return default


def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(value, maximum)
    )


def calculate_entropy(text):

    if not text:
        return 0.0

    frequencies = {}

    for character in text:

        frequencies[character] = (
            frequencies.get(character, 0) + 1
        )

    length = len(text)

    entropy = 0.0

    for count in frequencies.values():

        probability = count / length

        entropy -= (
            probability
            * math.log2(probability)
        )

    return round(
        entropy,
        4
    )


def normalize_whitespace(text):

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


def safe_decode(value):

    if not value:
        return ""

    result = value

    for _ in range(3):

        try:

            decoded = unquote(result)

        except Exception:

            break

        if decoded == result:
            break

        result = decoded

    return result


def sha256_text(text):

    return hashlib.sha256(
        text.encode(
            "utf-8",
            errors="ignore"
        )
    ).hexdigest()


# ============================================================
# URL ANALYZER
# ============================================================

class PhishingAnalyzer:

    def __init__(
        self,
        url,
        timeout=DEFAULT_TIMEOUT,
        fetch_content=True,
        verify_tls=True
    ):

        self.original_url = (
            url.strip()
            if isinstance(url, str)
            else ""
        )

        self.url = ""

        self.timeout = timeout
        self.fetch_content = fetch_content
        self.verify_tls = verify_tls

        self.parsed = None

        self.hostname = ""
        self.domain = ""
        self.scheme = ""
        self.port = None
        self.path = ""
        self.query = ""
        self.fragment = ""

        self.username = ""
        self.password = ""

        self.response = None

        self.html = ""

        self.headers = {}

        self.cookies = []

        self.redirect_chain = []

        self.findings = []

        self.errors = []

        self.warnings = []

        self.info = []

        self.metrics = {}

        self.score = 0

        self.start_time = time.time()
        self.is_verified_official = False
        self.ethical_hacking_profile = {
            "mitre_tactics": [],
            "mitre_techniques": [],
            "targeted_brand": None,
            "attack_vector": "None detected",
            "soc_remediation": []
        }


    # ========================================================
    # FINDING MANAGEMENT
    # ========================================================

    def add_score(self, value):

        value = safe_int(
            value,
            0
        )

        self.score = clamp(
            self.score + value,
            0,
            100
        )


    def add_finding(
        self,
        category,
        severity,
        title,
        description,
        evidence="",
        recommendation="",
        score=0,
        confidence="MEDIUM"
    ):

        finding = Finding(

            category=category,

            severity=severity,

            title=title,

            description=description,

            evidence=evidence,

            recommendation=recommendation,

            score=score,

            confidence=confidence

        )

        self.findings.append(
            finding
        )

        self.add_score(
            score
        )


    def add_warning(self, message):

        if message not in self.warnings:

            self.warnings.append(
                message
            )


    def add_error(self, message):

        if message not in self.errors:

            self.errors.append(
                message
            )


    def add_info(self, message):

        if message not in self.info:

            self.info.append(
                message
            )


    # ========================================================
    # URL NORMALIZATION
    # ========================================================

    def normalize_url(self):

        if not self.original_url:

            self.add_error(
                "URL is empty."
            )

            return False


        raw = self.original_url.strip()


        if not re.match(
            r"^[a-zA-Z][a-zA-Z0-9+\-.]*://",
            raw
        ):

            raw = "http://" + raw


        raw = raw.replace(
            " ",
            "%20"
        )


        try:

            parsed = urlsplit(
                raw
            )

        except Exception as error:

            self.add_error(
                f"URL parsing failed: {error}"
            )

            return False


        if not parsed.hostname:

            self.add_error(
                "URL does not contain a valid hostname."
            )

            return False


        try:

            hostname = parsed.hostname.lower()

        except Exception:

            hostname = ""


        self.parsed = parsed

        self.hostname = hostname

        self.scheme = (
            parsed.scheme.lower()
        )

        self.path = parsed.path or "/"

        self.query = parsed.query or ""

        self.fragment = parsed.fragment or ""


        try:

            self.port = parsed.port

        except ValueError:

            self.add_error(
                "Invalid port number in URL."
            )

            self.port = None


        try:

            self.username = (
                parsed.username or ""
            )

        except Exception:

            self.username = ""


        try:

            self.password = (
                parsed.password or ""
            )

        except Exception:

            self.password = ""


        try:

            self.url = urlunsplit(
                (
                    self.scheme,
                    parsed.netloc,
                    self.path,
                    self.query,
                    self.fragment
                )
            )

        except Exception:

            self.url = raw


        hostname_parts = [
            part
            for part in self.hostname.split(".")
            if part
        ]


        if len(hostname_parts) >= 2:

            self.domain = ".".join(
                hostname_parts[-2:]
            )

        else:

            self.domain = self.hostname


        return True


    # ========================================================
    # BASIC URL ANALYSIS
    # ========================================================

    def analyze_basic_url(self):

        if not self.parsed:
            return


        self.metrics["url_length"] = len(
            self.url
        )

        self.metrics["hostname_length"] = len(
            self.hostname
        )

        self.metrics["path_length"] = len(
            self.path
        )

        self.metrics["query_length"] = len(
            self.query
        )


        if len(self.url) > 150:

            self.add_finding(

                "URL Structure",

                "MEDIUM",

                "Very long URL",

                "The URL is unusually long and may hide suspicious parameters or encoded content.",

                evidence=f"URL length: {len(self.url)} characters",

                recommendation="Inspect the complete URL and verify that every parameter is expected.",

                score=5,

                confidence="MEDIUM"

            )


        if len(self.url) > 250:

            self.add_finding(

                "URL Structure",

                "HIGH",

                "Extremely long URL",

                "The URL is extremely long and may contain obfuscated or unnecessary data.",

                evidence=f"URL length: {len(self.url)} characters",

                recommendation="Avoid following the URL unless its complete destination is trusted.",

                score=8,

                confidence="MEDIUM"

            )


        if self.scheme not in {
            "http",
            "https"
        }:

            self.add_finding(

                "URL Structure",

                "MEDIUM",

                "Unusual URL scheme",

                "The URL uses a scheme that is not normal HTTP or HTTPS web traffic.",

                evidence=f"Scheme: {self.scheme}",

                recommendation="Only open the URL if the application specifically requires this scheme.",

                score=6,

                confidence="HIGH"

            )


        if self.scheme == "http":

            self.add_finding(

                "Transport Security",

                "LOW",

                "HTTP connection",

                "The URL uses HTTP instead of HTTPS.",

                evidence=self.url,

                recommendation="Prefer HTTPS when sensitive information is involved.",

                score=3,

                confidence="HIGH"

            )


        if self.username or self.password:

            self.add_finding(

                "URL Obfuscation",

                "HIGH",

                "User information embedded in URL",

                "The URL contains user information before the hostname. Attackers can abuse this format to make URLs misleading.",

                evidence=f"User information detected before host: {self.hostname}",

                recommendation="Do not trust a URL simply because a familiar-looking name appears before the @ symbol.",

                score=12,

                confidence="HIGH"

            )


    # ========================================================
    # IP ADDRESS ANALYSIS
    # ========================================================

    def is_ip_address(self, hostname=None):

        hostname = (
            hostname
            if hostname is not None
            else self.hostname
        )


        if not hostname:
            return False


        try:

            ipaddress.ip_address(
                hostname
            )

            return True

        except ValueError:

            return False


    def analyze_ip(self):

        if not self.hostname:
            return


        if not self.is_ip_address():
            return


        try:

            ip_obj = ipaddress.ip_address(
                self.hostname
            )

            version = ip_obj.version

            self.metrics["ip_version"] = version


            if ip_obj.is_private:

                self.add_info(
                    "Target is a private IP address."
                )


            elif ip_obj.is_loopback:

                self.add_warning(
                    "Target is a loopback address."
                )


            elif ip_obj.is_link_local:

                self.add_warning(
                    "Target is a link-local address."
                )


            elif ip_obj.is_reserved:

                self.add_warning(
                    "Target is a reserved IP address."
                )


            else:

                self.add_finding(

                    "Domain Identity",

                    "MEDIUM",

                    "URL uses an IP address",

                    "The URL directly uses an IP address instead of a normal domain name.",

                    evidence=self.hostname,

                    recommendation="Verify the destination independently before opening the URL.",

                    score=7,

                    confidence="MEDIUM"

                )


        except Exception as error:

            self.add_error(
                f"IP analysis failed: {error}"
            )


    # ========================================================
    # DOMAIN ANALYSIS
    # ========================================================

    def analyze_domain(self):

        if not self.hostname:
            return


        hostname = self.hostname.lower()


        if len(hostname) > 50:

            self.add_finding(

                "Domain Structure",

                "MEDIUM",

                "Long hostname",

                "The hostname is unusually long.",

                evidence=f"Hostname length: {len(hostname)}",

                recommendation="Check the complete hostname carefully before trusting it.",

                score=4,

                confidence="MEDIUM"

            )


        labels = [
            label
            for label in hostname.split(".")
            if label
        ]


        self.metrics["subdomain_count"] = max(
            len(labels) - 2,
            0
        )


        self.metrics["domain_labels"] = len(
            labels
        )


        if len(labels) >= 5:

            self.add_finding(

                "Domain Structure",

                "MEDIUM",

                "Many subdomains",

                "The hostname contains many labels, which can make the real domain harder to notice.",

                evidence=hostname,

                recommendation="Read the hostname from right to left and identify the actual registered domain.",

                score=5,

                confidence="MEDIUM"

            )


        repeated_separator = (
            ".." in hostname
        )


        if repeated_separator:

            self.add_finding(

                "Domain Structure",

                "MEDIUM",

                "Repeated domain separator",

                "The hostname contains consecutive dots.",

                evidence=hostname,

                recommendation="Treat malformed or unusual hostnames with caution.",

                score=4,

                confidence="HIGH"

            )


        if "--" in hostname:

            self.add_warning(
                "Hostname contains consecutive hyphens."
            )


        digit_count = sum(
            1
            for character in hostname
            if character.isdigit()
        )


        self.metrics["hostname_digit_count"] = (
            digit_count
        )


        if digit_count >= 8:

            self.add_finding(

                "Domain Structure",

                "MEDIUM",

                "High number of digits in hostname",

                "The hostname contains many numeric characters.",

                evidence=f"Digit count: {digit_count}",

                recommendation="Verify that the numeric hostname is expected and belongs to the claimed service.",

                score=5,

                confidence="LOW"

            )


    # ========================================================
    # TLD ANALYSIS
    # ========================================================

    def analyze_tld(self):

        if not self.hostname:
            return


        parts = self.hostname.split(".")


        if len(parts) < 2:
            return


        tld = parts[-1].lower()


        self.metrics["tld"] = tld


        if tld in SUSPICIOUS_TLDS:

            self.add_finding(

                "Domain Reputation",

                "LOW",

                "TLD commonly seen in suspicious URLs",

                "The top-level domain has been observed in many low-cost or abuse-prone registrations.",

                evidence=f"TLD: .{tld}",

                recommendation="Do not judge the site only by its TLD; verify the organization independently.",

                score=3,

                confidence="LOW"

            )


    # ========================================================
    # PUNYCODE / UNICODE ANALYSIS
    # ========================================================

    def analyze_punycode(self):

        if not self.hostname:
            return


        if "xn--" in self.hostname.lower():

            self.add_finding(

                "Domain Obfuscation",

                "HIGH",

                "Punycode domain detected",

                "The hostname contains an internationalized domain encoded with Punycode.",

                evidence=self.hostname,

                recommendation="Inspect the displayed domain carefully because visually similar Unicode characters can be abused for impersonation.",

                score=10,

                confidence="HIGH"

            )


        try:

            unicode_form = unicodedata.normalize(
                "NFKC",
                self.hostname
            )

            self.metrics["normalized_hostname"] = (
                unicode_form
            )


            non_ascii = [
                character
                for character in self.hostname
                if ord(character) > 127
            ]


            if non_ascii:

                self.add_finding(

                    "Domain Obfuscation",

                    "MEDIUM",

                    "Non-ASCII hostname characters",

                    "The hostname contains Unicode characters.",

                    evidence="".join(non_ascii),

                    recommendation="Verify the domain spelling and ownership before trusting it.",

                    score=7,

                    confidence="MEDIUM"

                )


        except Exception as error:

            self.add_warning(
                f"Unicode hostname analysis failed: {error}"
            )


    # ========================================================
    # BRAND ANALYSIS
    # ========================================================

    def analyze_brands(self):
        if not self.hostname:
            return

        host = self.hostname.lower()
        parts = host.split(".")
        reg_domain = ".".join(parts[-2:]) if len(parts) >= 2 else host
        domain_body = parts[-2] if len(parts) >= 2 else host

        # 1. Check if the domain is verified official brand domain
        for brand, officials in OFFICIAL_BRAND_DOMAINS.items():
            if reg_domain in officials or host in officials:
                self.is_verified_official = True
                self.metrics["brand_mentions"] = [brand]
                self.metrics["brand_status"] = f"VERIFIED OFFICIAL {brand.upper()}"
                self.add_info(f"Verified official domain for {brand.upper()} ({reg_domain}). Zero spoofing detected.")
                return

        # 2. Check Combosquatting: brand keyword present in hostname on non-official domain
        detected_brands = []
        for brand, officials in OFFICIAL_BRAND_DOMAINS.items():
            if brand in host and reg_domain not in officials:
                detected_brands.append(brand)

        if detected_brands:
            detected_brands = sorted(list(set(detected_brands)))
            primary_brand = detected_brands[0]
            self.metrics["brand_mentions"] = detected_brands
            self.ethical_hacking_profile["targeted_brand"] = primary_brand.upper()
            self.ethical_hacking_profile["attack_vector"] = f"Combosquatting brand impersonation targeting {primary_brand.upper()}"
            self.add_finding(
                "Targeted Brand Impersonation (Combosquatting)",
                "CRITICAL",
                f"Unauthorized brand domain targeting {primary_brand.upper()}",
                f"The hostname '{host}' incorporates the high-value brand '{primary_brand}' on an unregistered, non-official domain '{reg_domain}'. This is a high-confidence combosquatting vector frequently utilized in credential harvesting.",
                evidence=f"Brand: {primary_brand}, Host: {host}, Registered Domain: {reg_domain}",
                recommendation=f"Do not interact or enter credentials. Legitimate {primary_brand.upper()} services operate strictly under verified domains.",
                score=65,
                confidence="HIGH"
            )

        # 3. Check Leetspeak Substitutions in domain body (e.g. paypa1, micros0ft, arnazon, goog1e)
        norm_body = normalize_leetspeak(domain_body)
        for brand, officials in OFFICIAL_BRAND_DOMAINS.items():
            if brand in norm_body and brand not in domain_body and reg_domain not in officials:
                self.ethical_hacking_profile["targeted_brand"] = brand.upper()
                self.ethical_hacking_profile["attack_vector"] = f"Leetspeak character substitution typosquatting targeting {brand.upper()}"
                self.add_finding(
                    "Obfuscated Typosquatting (Leetspeak)",
                    "CRITICAL",
                    f"Leetspeak visual homoglyph targeting {brand.upper()}",
                    f"Domain label '{domain_body}' utilizes deceptive leetspeak substitutions (e.g., '1' for 'l', '0' for 'o', or 'rn' for 'm') to masquerade visually as '{brand}'.",
                    evidence=f"Spoofed label: '{domain_body}', Normalized: '{norm_body}', Target: '{brand}'",
                    recommendation="Immediately block this domain at the perimeter firewall and email gateway.",
                    score=70,
                    confidence="HIGH"
                )
                break

        # 4. Check Fuzzy Typosquatting (Damerau-Levenshtein edit distance 1-2)
        # Always runs — even if combosquatting/leetspeak already fired, typosquat is independent evidence
        if not self.ethical_hacking_profile.get("targeted_brand"):
            best_dist = 99
            best_brand = None
            for brand, officials in OFFICIAL_BRAND_DOMAINS.items():
                if reg_domain in officials:
                    continue  # official domain — skip
                dist = calculate_levenshtein(domain_body, brand)
                if 1 <= dist <= 2 and len(brand) >= 4 and abs(len(domain_body) - len(brand)) <= 2:
                    if dist < best_dist:
                        best_dist = dist
                        best_brand = brand
            if best_brand:
                self.ethical_hacking_profile["targeted_brand"] = best_brand.upper()
                self.ethical_hacking_profile["attack_vector"] = f"Fuzzy domain typosquatting targeting {best_brand.upper()}"
                self.add_finding(
                    "Fuzzy Domain Typosquatting",
                    "CRITICAL",
                    f"Domain typosquatting within {best_dist} character(s) of {best_brand.upper()}",
                    f"The domain label '{domain_body}' closely resembles the trademarked entity '{best_brand}' with an edit distance of {best_dist}, consistent with look-alike spoofing domains used in credential harvesting campaigns.",
                    evidence=f"Domain: '{domain_body}', Brand: '{best_brand}', Damerau-Levenshtein Distance: {best_dist}",
                    recommendation=f"Block this domain at the perimeter. Legitimate {best_brand.upper()} services do not operate from this domain.",
                    score=63,
                    confidence="HIGH"
                )
    # ========================================================
    # KEYWORD ANALYSIS
    # ========================================================

    def analyze_keywords(self):

        target = " ".join(
            [
                self.hostname,
                self.path,
                self.query
            ]
        ).lower()


        decoded = safe_decode(
            target
        ).lower()


        detected = {}

        total = 0


        for keyword, weight in SUSPICIOUS_KEYWORDS.items():

            if keyword in decoded:

                detected[keyword] = weight

                total += weight


        self.metrics["suspicious_keywords"] = (
            detected
        )


        self.metrics["keyword_score"] = total


        if not detected:
            return


        sorted_keywords = sorted(
            detected.keys()
        )


        self.add_info(

            "Suspicious URL keywords: "
            + ", ".join(sorted_keywords)

        )


        if total >= 12:

            severity = "HIGH"

            score = 10

        elif total >= 7:

            severity = "MEDIUM"

            score = 6

        else:

            severity = "LOW"

            score = 3


        self.add_finding(

            "URL Content",

            severity,

            "Security-sensitive keywords detected",

            "The URL contains words frequently associated with login, verification, account, payment, or urgency themes.",

            evidence=", ".join(
                sorted_keywords
            ),

            recommendation="Confirm that the URL belongs to the organization it claims to represent.",

            score=score,

            confidence="LOW"

        )


    # ========================================================
    # ENTROPY ANALYSIS
    # ========================================================

    def analyze_entropy(self):

        hostname_entropy = calculate_entropy(
            self.hostname
        )

        path_entropy = calculate_entropy(
            self.path
        )

        query_entropy = calculate_entropy(
            self.query
        )


        self.metrics["hostname_entropy"] = (
            hostname_entropy
        )

        self.metrics["path_entropy"] = (
            path_entropy
        )

        self.metrics["query_entropy"] = (
            query_entropy
        )


        if hostname_entropy >= 4.0:

            self.add_finding(

                "URL Obfuscation",

                "MEDIUM",

                "High hostname entropy",

                "The hostname contains a relatively high variety of characters, which can sometimes indicate generated or obfuscated domains.",

                evidence=f"Entropy: {hostname_entropy}",

                recommendation="Verify the domain ownership and spelling.",

                score=4,

                confidence="LOW"

            )


        if query_entropy >= 5.0:

            self.add_warning(
                "URL query contains high-entropy data."
            )


    # ========================================================
    # SHORTENER ANALYSIS
    # ========================================================

    def analyze_shortener(self):

        if not self.hostname:
            return


        host = self.hostname.lower()


        if host in SHORTENER_DOMAINS:

            self.add_finding(

                "URL Redirection",

                "MEDIUM",

                "URL shortener detected",

                "The URL uses a known URL-shortening service.",

                evidence=host,

                recommendation="Resolve the final destination before trusting the shortened URL.",

                score=7,

                confidence="HIGH"

            )


    # ========================================================
    # PORT ANALYSIS
    # ========================================================

    def analyze_port(self):

        if self.port is None:
            return


        self.metrics["port"] = (
            self.port
        )


        if self.port in SUSPICIOUS_PORTS:

            if self.port not in COMMON_WEB_PORTS:

                self.add_finding(

                    "Network Exposure",

                    "LOW",

                    "Non-standard web port",

                    "The URL uses a port that is not a typical public web port.",

                    evidence=f"Port: {self.port}",

                    recommendation="Verify that the service is intentionally exposed on this port.",

                    score=3,

                    confidence="MEDIUM"

                )


    # ========================================================
    # PARAMETER ANALYSIS
    # ========================================================

    def analyze_parameters(self):

        if not self.query:

            self.metrics["parameter_count"] = 0

            return


        try:

            parameters = parse_qsl(
                self.query,
                keep_blank_values=True
            )

        except Exception as error:

            self.add_warning(
                f"Query parameter parsing failed: {error}"
            )

            return


        self.metrics["parameter_count"] = len(
            parameters
        )


        parameter_names = [
            name.lower()
            for name, _ in parameters
        ]


        self.metrics["parameter_names"] = (
            parameter_names
        )


        redirect_parameters = []

        tracking_parameters = []


        for name in parameter_names:

            if name in REDIRECT_PARAMETERS:

                redirect_parameters.append(
                    name
                )

            if name in TRACKING_PARAMETERS:

                tracking_parameters.append(
                    name
                )


        self.metrics["redirect_parameters"] = (
            redirect_parameters
        )

        self.metrics["tracking_parameters"] = (
            tracking_parameters
        )


        if redirect_parameters:

            self.add_finding(

                "URL Redirection",

                "MEDIUM",

                "Redirect parameter detected",

                "The URL contains a parameter commonly used to redirect visitors to another destination.",

                evidence=", ".join(
                    redirect_parameters
                ),

                recommendation="Inspect the parameter value and verify the final destination.",

                score=5,

                confidence="MEDIUM"

            )


        if tracking_parameters:

            self.add_info(

                "Tracking parameters detected: "
                + ", ".join(tracking_parameters)

            )


        suspicious_values = []


        for name, value in parameters:

            decoded_value = safe_decode(
                value
            ).lower()


            if (
                "javascript:" in decoded_value
                or "<script" in decoded_value
                or "data:text/html" in decoded_value
            ):

                suspicious_values.append(
                    name
                )


        if suspicious_values:

            self.add_finding(

                "URL Obfuscation",

                "HIGH",

                "Suspicious parameter content",

                "A URL parameter contains content resembling executable or HTML data.",

                evidence=", ".join(
                    suspicious_values
                ),

                recommendation="Do not open the URL unless the parameter is expected and trusted.",

                score=10,

                confidence="HIGH"

            )


    # ========================================================
    # PATH ANALYSIS
    # ========================================================

    def analyze_path(self):

        path = safe_decode(
            self.path
        )


        self.metrics["decoded_path"] = (
            path
        )


        extension_matches = []


        lower_path = path.lower()


        for extension in SUSPICIOUS_EXTENSIONS:

            if lower_path.endswith(
                extension
            ):

                extension_matches.append(
                    extension
                )


        if extension_matches:

            self.add_finding(

                "URL Content",

                "MEDIUM",

                "Suspicious file extension",

                "The URL path ends with a file extension that can be associated with downloadable or executable content.",

                evidence=", ".join(
                    extension_matches
                ),

                recommendation="Do not download files unless the source is verified.",

                score=7,

                confidence="MEDIUM"

            )


        path_segments = [
            segment
            for segment in path.split("/")
            if segment
        ]


        self.metrics["path_segments"] = (
            len(path_segments)
        )


        if len(path_segments) > 12:

            self.add_finding(

                "URL Structure",

                "LOW",

                "Deep URL path",

                "The URL contains an unusually deep path.",

                evidence=f"Path segments: {len(path_segments)}",

                recommendation="Inspect the complete URL and destination before trusting it.",

                score=3,

                confidence="LOW"

            )


        repeated_slashes = (
            "//" in path
        )


        if repeated_slashes:

            self.add_warning(
                "URL path contains repeated slashes."
            )


    # ========================================================
    # ENCODING ANALYSIS
    # ========================================================

    def analyze_encoding(self):

        encoded_count = len(
            re.findall(
                r"%[0-9a-fA-F]{2}",
                self.url
            )
        )


        self.metrics["percent_encoded_count"] = (
            encoded_count
        )


        if encoded_count >= 10:

            self.add_finding(

                "URL Obfuscation",

                "MEDIUM",

                "Heavy percent encoding",

                "The URL contains a large number of percent-encoded characters.",

                evidence=f"Encoded characters: {encoded_count}",

                recommendation="Decode and inspect the URL before trusting it.",

                score=6,

                confidence="MEDIUM"

            )


        decoded = safe_decode(
            self.url
        )


        if decoded != self.url:

            self.metrics["decoded_url"] = (
                decoded
            )


        try:

            if re.search(
                r"%25[0-9a-fA-F]{2}",
                self.url
            ):

                self.add_finding(

                    "URL Obfuscation",

                    "MEDIUM",

                    "Double URL encoding detected",

                    "The URL appears to contain double-encoded characters.",

                    evidence="Double percent encoding pattern detected",

                    recommendation="Decode the URL carefully before following it.",

                    score=5,

                    confidence="MEDIUM"

                )

        except Exception:
            pass


    # ========================================================
    # SPECIAL CHARACTER ANALYSIS
    # ========================================================

    def analyze_special_characters(self):

        if not self.url:
            return


        counts = {

            "@": self.url.count("@"),

            "-": self.hostname.count("-"),

            "_": self.hostname.count("_"),

            ".": self.hostname.count("."),

            "%": self.url.count("%"),

            "=": self.url.count("="),

            "&": self.url.count("&"),

            "?": self.url.count("?")

        }


        self.metrics["special_character_counts"] = (
            counts
        )


        if counts["@"]:

            self.add_finding(

                "URL Obfuscation",

                "HIGH",

                "At-sign present in URL",

                "The at-sign can separate user information from the actual hostname and is frequently abused in deceptive URLs.",

                evidence=f"At-sign count: {counts['@']}",

                recommendation="Identify the actual hostname after the @ symbol.",

                score=8,

                confidence="HIGH"

            )


        if counts["="] >= 8:

            self.add_warning(
                "URL contains many query assignments."
            )


        if counts["&"] >= 10:

            self.add_warning(
                "URL contains many query parameters."
            )


    # ========================================================
    # DNS ANALYSIS
    # ========================================================

    def analyze_dns(self):

        if not self.hostname:
            return


        if self.is_ip_address():

            self.metrics["dns_resolution"] = (
                "Not required for IP address"
            )

            return


        try:

            start = time.time()


            addresses = socket.getaddrinfo(
                self.hostname,
                self.port or (
                    443
                    if self.scheme == "https"
                    else 80
                ),
                type=socket.SOCK_STREAM
            )


            elapsed = (
                time.time() - start
            ) * 1000


            resolved = sorted(
                {
                    result[4][0]
                    for result in addresses
                    if result and result[4]
                }
            )


            self.metrics["dns_addresses"] = (
                resolved
            )

            self.metrics["dns_resolution_ms"] = round(
                elapsed,
                2
            )


            if resolved:

                self.add_info(

                    "DNS resolved to: "
                    + ", ".join(resolved)

                )


        except socket.gaierror as error:

            self.add_finding(

                "Domain Resolution",

                "MEDIUM",

                "DNS resolution failed",

                "The hostname could not be resolved through the local DNS resolver.",

                evidence=str(error),

                recommendation="Verify the domain spelling and availability.",

                score=4,

                confidence="MEDIUM"

            )

        except Exception as error:

            self.add_warning(
                f"DNS analysis failed: {error}"
            )


    # ========================================================
    # URL LAYER SCAN
    # ========================================================
# ========================================================
# MAIN URL SCAN
# ========================================================

    def scan_url_layer(self):

        checks = [
            self.analyze_basic_url,
            self.analyze_ip,
            self.analyze_domain,
            self.analyze_tld,
            self.analyze_punycode,
            self.analyze_brands,
            self.analyze_keywords,
            self.analyze_entropy,
            self.analyze_shortener,
            self.analyze_port,
            self.analyze_parameters,
            self.analyze_path,
            self.analyze_encoding,
            self.analyze_special_characters
        ]

        # DNS lookup is a network operation.
        # Only perform it during full analysis.
        if self.fetch_content:
            checks.append(
                self.analyze_dns
            )

        for check in checks:

            try:

                check()

            except Exception as error:

                self.add_error(
                    f"{check.__name__}: {error}"
                )
    

# ============================================================
# END OF PART 1
# ============================================================
# ============================================================
# HTTP / PAGE ANALYSIS
# ============================================================

    def fetch_page(self):

        if requests is None:

            self.add_error(
                "The requests library is not installed. "
                "Run: pip install requests"
            )

            return False


        if not self.url:

            self.add_error(
                "Cannot fetch page because the URL is not valid."
            )

            return False


        request_headers = {

            "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36 "
                "NIGHT-HUNTER/3.0",

            "Accept":
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8",

            "Accept-Language":
                "en-US,en;q=0.8",

            "Connection":
                "close"

        }


        session = requests.Session()

        session.headers.update(
            request_headers
        )


        try:

            start_time = time.time()


            response = session.get(

                self.url,

                timeout=self.timeout,

                allow_redirects=True,

                verify=self.verify_tls,

                stream=True

            )


            elapsed = (
                time.time() - start_time
            ) * 1000


            self.response = response


            # ------------------------------------------------
            # RESPONSE INFORMATION
            # ------------------------------------------------

            self.headers = {

                str(key): str(value)

                for key, value
                in response.headers.items()

            }


            self.metrics["http_status"] = (
                response.status_code
            )

            self.metrics["response_time_ms"] = round(
                elapsed,
                2
            )

            self.metrics["final_url"] = (
                response.url
            )

            self.metrics["content_type"] = (
                response.headers.get(
                    "Content-Type",
                    ""
                )
            )

            self.metrics["server"] = (
                response.headers.get(
                    "Server",
                    ""
                )
            )

            self.metrics["x_powered_by"] = (
                response.headers.get(
                    "X-Powered-By",
                    ""
                )
            )


            # ------------------------------------------------
            # REDIRECT CHAIN
            # ------------------------------------------------

            self.redirect_chain = []


            for redirect_response in response.history:

                self.redirect_chain.append({

                    "status_code":
                        redirect_response.status_code,

                    "url":
                        redirect_response.url,

                    "location":
                        redirect_response.headers.get(
                            "Location",
                            ""
                        )

                })


            self.redirect_chain.append({

                "status_code":
                    response.status_code,

                "url":
                    response.url,

                "location":
                    ""

            })


            self.metrics["redirect_count"] = (
                len(response.history)
            )


            if response.history:

                self.add_finding(

                    "HTTP Redirect",

                    "LOW",

                    "Redirect chain detected",

                    "The target redirected the request through one or more URLs.",

                    evidence=
                        f"{len(response.history)} redirect(s)",

                    recommendation=
                        "Review the complete redirect chain and verify the final domain.",

                    score=3,

                    confidence="HIGH"

                )


            if len(response.history) >= 5:

                self.add_finding(

                    "HTTP Redirect",

                    "MEDIUM",

                    "Long redirect chain",

                    "The target uses several redirects before reaching the final destination.",

                    evidence=
                        f"{len(response.history)} redirects",

                    recommendation=
                        "Verify every redirect destination before trusting the final page.",

                    score=5,

                    confidence="MEDIUM"

                )


            if len(response.history) >= MAX_REDIRECTS:

                self.add_finding(

                    "HTTP Redirect",

                    "HIGH",

                    "Redirect limit reached",

                    "The request reached the configured maximum redirect limit.",

                    evidence=
                        f"Maximum redirects: {MAX_REDIRECTS}",

                    recommendation=
                        "Do not follow the destination until the redirect chain is understood.",

                    score=10,

                    confidence="HIGH"

                )


            # ------------------------------------------------
            # FINAL URL
            # ------------------------------------------------

            final_url = response.url


            if final_url != self.url:

                self.add_info(

                    "Final destination: "
                    + final_url

                )


                try:

                    original_host = (
                        urlsplit(
                            self.url
                        ).hostname or ""
                    ).lower()


                    final_host = (
                        urlsplit(
                            final_url
                        ).hostname or ""
                    ).lower()


                    if (
                        original_host
                        and final_host
                        and original_host != final_host
                    ):

                        self.add_finding(

                            "Domain Redirect",

                            "MEDIUM",

                            "Redirect changed hostname",

                            "The request ended on a different hostname than the original URL.",

                            evidence=
                                f"{original_host} -> {final_host}",

                            recommendation=
                                "Verify that the hostname change is expected.",

                            score=6,

                            confidence="HIGH"

                        )


                except Exception:

                    pass


            # ------------------------------------------------
            # HTTP STATUS
            # ------------------------------------------------

            status = response.status_code


            if status >= 500:

                self.add_warning(
                    f"Server returned HTTP {status}."
                )

            elif status >= 400:

                self.add_warning(
                    f"Target returned HTTP {status}."
                )

            elif status >= 300:

                self.add_info(
                    f"Target returned HTTP {status}."
                )

            elif 200 <= status < 300:

                self.add_info(
                    f"Successful HTTP response: {status}."
                )


            # ------------------------------------------------
            # SECURITY HEADERS
            # ------------------------------------------------

            self.analyze_security_headers()


            # ------------------------------------------------
            # SERVER DISCLOSURE
            # ------------------------------------------------

            self.analyze_server_headers()


            # ------------------------------------------------
            # CONTENT TYPE
            # ------------------------------------------------

            content_type = response.headers.get(
                "Content-Type",
                ""
            ).lower()


            if (
                "text/html" not in content_type
                and
                "application/xhtml+xml"
                not in content_type
            ):

                self.add_info(

                    "Response is not an HTML document: "
                    + (
                        content_type
                        or "unknown"
                    )

                )

                self.metrics["downloaded_bytes"] = 0

                return True


            # ------------------------------------------------
            # READ RESPONSE SAFELY
            # ------------------------------------------------

            chunks = []

            total_size = 0


            for chunk in response.iter_content(
                chunk_size=8192,
                decode_unicode=False
            ):

                if not chunk:
                    continue


                remaining = (
                    MAX_CONTENT_SIZE
                    - total_size
                )


                if remaining <= 0:
                    break


                chunk = chunk[:remaining]


                chunks.append(
                    chunk
                )


                total_size += len(
                    chunk
                )


                if total_size >= MAX_CONTENT_SIZE:
                    break


            raw_content = b"".join(
                chunks
            )


            self.metrics["downloaded_bytes"] = (
                len(raw_content)
            )


            self.metrics["content_truncated"] = (
                len(raw_content)
                >= MAX_CONTENT_SIZE
            )


            encoding = (
                response.encoding
                or "utf-8"
            )


            try:

                self.html = raw_content.decode(
                    encoding,
                    errors="replace"
                )

            except LookupError:

                self.html = raw_content.decode(
                    "utf-8",
                    errors="replace"
                )


            # ------------------------------------------------
            # HTML ANALYSIS
            # ------------------------------------------------

            self.analyze_html()


            # ------------------------------------------------
            # COOKIE ANALYSIS
            # ------------------------------------------------

            self.analyze_cookies()


            return True


        except requests.exceptions.SSLError as error:

            self.add_error(
                f"TLS/SSL error: {error}"
            )


        except requests.exceptions.Timeout:

            self.add_error(
                f"Request timed out after "
                f"{self.timeout} seconds."
            )


        except requests.exceptions.TooManyRedirects:

            self.add_error(
                "Too many HTTP redirects."
            )


        except requests.exceptions.ConnectionError as error:

            self.add_error(
                f"Connection failed: {error}"
            )


        except requests.exceptions.RequestException as error:

            self.add_error(
                f"HTTP request failed: {error}"
            )


        except Exception as error:

            self.add_error(
                f"Page fetch failed: {error}"
            )


        return False


    # ========================================================
    # SECURITY HEADER ANALYSIS
    # ========================================================

    def analyze_security_headers(self):

        if not self.headers:
            return


        header_map = {

            key.lower(): value

            for key, value
            in self.headers.items()

        }


        security_headers = {

            "content-security-policy":
                "Content-Security-Policy",

            "strict-transport-security":
                "Strict-Transport-Security",

            "x-content-type-options":
                "X-Content-Type-Options",

            "x-frame-options":
                "X-Frame-Options",

            "referrer-policy":
                "Referrer-Policy",

            "permissions-policy":
                "Permissions-Policy"

        }


        present = []

        missing = []


        for lower_name, display_name in security_headers.items():

            if lower_name in header_map:

                present.append(
                    display_name
                )

            else:

                missing.append(
                    display_name
                )


        self.metrics["security_headers_present"] = (
            present
        )

        self.metrics["security_headers_missing"] = (
            missing
        )


        if missing:

            self.add_info(

                "Missing security headers: "
                + ", ".join(missing)

            )


        # ----------------------------------------------------
        # CSP
        # ----------------------------------------------------

        if (
            "content-security-policy"
            not in header_map
        ):

            self.add_finding(

                "HTTP Security",

                "LOW",

                "Content-Security-Policy missing",

                "The response does not provide a Content-Security-Policy header.",

                evidence="CSP header not found",

                recommendation=
                    "Consider deploying an appropriate Content-Security-Policy.",

                score=2,

                confidence="HIGH"

            )


        # ----------------------------------------------------
        # HSTS
        # ----------------------------------------------------

        if (
            self.scheme == "https"
            and
            "strict-transport-security"
            not in header_map
        ):

            self.add_finding(

                "HTTP Security",

                "LOW",

                "HSTS header missing",

                "The HTTPS response does not provide Strict-Transport-Security.",

                evidence="HSTS header not found",

                recommendation=
                    "Consider enabling HSTS for HTTPS deployments.",

                score=2,

                confidence="HIGH"

            )


        # ----------------------------------------------------
        # X-CONTENT-TYPE
        # ----------------------------------------------------

        if (
            "x-content-type-options"
            not in header_map
        ):

            self.add_finding(

                "HTTP Security",

                "LOW",

                "X-Content-Type-Options missing",

                "The response does not explicitly disable MIME type sniffing.",

                evidence=
                    "X-Content-Type-Options header not found",

                recommendation=
                    "Consider setting X-Content-Type-Options to nosniff.",

                score=1,

                confidence="HIGH"

            )


        # ----------------------------------------------------
        # FRAME OPTIONS
        # ----------------------------------------------------

        if (
            "x-frame-options"
            not in header_map
            and
            "content-security-policy"
            not in header_map
        ):

            self.add_finding(

                "HTTP Security",

                "LOW",

                "Clickjacking protection not obvious",

                "Neither X-Frame-Options nor an obvious CSP header was found.",

                evidence=
                    "Frame protection headers not detected",

                recommendation=
                    "Review clickjacking protection for the application.",

                score=2,

                confidence="MEDIUM"

            )


    # ========================================================
    # SERVER HEADER ANALYSIS
    # ========================================================

    def analyze_server_headers(self):

        server = self.headers.get(
            "Server",
            ""
        )


        powered_by = self.headers.get(
            "X-Powered-By",
            ""
        )


        if server:

            self.add_info(
                f"Server header: {server}"
            )


        if powered_by:

            self.add_finding(

                "Information Disclosure",

                "LOW",

                "Technology disclosure header",

                "The response exposes an X-Powered-By header.",

                evidence=
                    powered_by,

                recommendation=
                    "Consider removing unnecessary technology disclosure headers.",

                score=2,

                confidence="HIGH"

            )


        server_lower = server.lower()


        version_pattern = re.search(
            r"([a-zA-Z_-]+)"
            r"/"
            r"([0-9]+(?:\.[0-9]+){1,3})",
            server
        )


        if version_pattern:

            self.add_finding(

                "Information Disclosure",

                "LOW",

                "Server version disclosure",

                "The Server header appears to disclose a software version.",

                evidence=server,

                recommendation=
                    "Consider reducing unnecessary version disclosure.",

                score=2,

                confidence="MEDIUM"

            )


        if "php" in server_lower:

            self.add_info(
                "PHP-related server information detected."
            )


        if "nginx" in server_lower:

            self.add_info(
                "Nginx server identified."
            )


        if "apache" in server_lower:

            self.add_info(
                "Apache server identified."
            )


        if "iis" in server_lower:

            self.add_info(
                "Microsoft IIS server identified."
            )


    # ========================================================
    # COOKIE ANALYSIS
    # ========================================================

    def analyze_cookies(self):

        if not self.response:
            return


        self.cookies = []


        try:

            for cookie in self.response.cookies:

                rest = getattr(
                    cookie,
                    "_rest",
                    {}
                )


                httponly = (

                    rest.get("HttpOnly")
                    or
                    rest.get("httponly")
                    or
                    rest.get("HTTPOnly")
                    or
                    False

                )


                samesite = (

                    rest.get("SameSite")
                    or
                    rest.get("samesite")
                    or
                    ""

                )


                cookie_data = {

                    "name":
                        cookie.name,

                    "domain":
                        cookie.domain,

                    "path":
                        cookie.path,

                    "secure":
                        bool(cookie.secure),

                    "httponly":
                        bool(httponly),

                    "samesite":
                        samesite

                }


                self.cookies.append(
                    cookie_data
                )


        except Exception as error:

            self.add_warning(
                f"Cookie analysis failed: {error}"
            )

            return


        self.metrics["cookie_count"] = (
            len(self.cookies)
        )


        if not self.cookies:
            return


        insecure_cookies = []


        for cookie in self.cookies:

            if (
                self.scheme == "https"
                and
                not cookie["secure"]
            ):

                insecure_cookies.append(
                    cookie["name"]
                )


        if insecure_cookies:

            self.add_finding(

                "Cookie Security",

                "MEDIUM",

                "Cookie without Secure flag",

                "One or more cookies were set without the Secure attribute on an HTTPS response.",

                evidence=
                    ", ".join(insecure_cookies),

                recommendation=
                    "Review sensitive cookies and enable Secure where appropriate.",

                score=5,

                confidence="HIGH"

            )


        httponly_missing = []


        for cookie in self.cookies:

            name = cookie["name"].lower()


            sensitive_name = any(

                word in name

                for word in (

                    "session",
                    "sess",
                    "auth",
                    "token",
                    "login",
                    "jwt"

                )

            )


            if (
                sensitive_name
                and
                not cookie["httponly"]
            ):

                httponly_missing.append(
                    cookie["name"]
                )


        if httponly_missing:

            self.add_finding(

                "Cookie Security",

                "MEDIUM",

                "Potentially sensitive cookie lacks HttpOnly",

                "A cookie with a session or authentication-like name does not appear to use HttpOnly.",

                evidence=
                    ", ".join(httponly_missing),

                recommendation=
                    "Review whether sensitive cookies should use HttpOnly.",

                score=5,

                confidence="MEDIUM"

            )


        samesite_missing = []


        for cookie in self.cookies:

            if not cookie["samesite"]:

                samesite_missing.append(
                    cookie["name"]
                )


        if samesite_missing:

            self.add_info(

                "Cookies without an explicit SameSite attribute: "
                + ", ".join(samesite_missing)

            )


    # ========================================================
    # HTML ANALYSIS
    # ========================================================

    def analyze_html(self):

        if not self.html:

            return


        html = self.html


        self.metrics["html_length"] = (
            len(html)
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_match = re.search(

            r"<title\b[^>]*>"
            r"(.*?)"
            r"</title>",

            html,

            re.IGNORECASE
            | re.DOTALL

        )


        title = ""


        if title_match:

            title = normalize_whitespace(
                re.sub(
                    r"<[^>]+>",
                    " ",
                    title_match.group(1)
                )
            )


        self.metrics["page_title"] = (
            title
        )


        if title:

            self.add_info(
                f"Page title: {title}"
            )


        # ----------------------------------------------------
        # FORMS
        # ----------------------------------------------------

        forms = re.findall(

            r"<form\b"
            r"([^>]*)>"
            r"(.*?)"
            r"</form>",

            html,

            re.IGNORECASE
            | re.DOTALL

        )


        self.metrics["form_count"] = (
            len(forms)
        )


        password_forms = []


        external_form_actions = []


        for attributes, body in forms:

            action_match = re.search(

                r"\baction\s*=\s*"
                r"""["']([^"']+)["']""",

                attributes,

                re.IGNORECASE

            )


            action = (

                action_match.group(1).strip()

                if action_match

                else ""

            )


            method_match = re.search(

                r"\bmethod\s*=\s*"
                r"""["']([^"']+)["']""",

                attributes,

                re.IGNORECASE

            )


            method = (

                method_match.group(1).lower()

                if method_match

                else "get"

            )


            password_inputs = re.findall(

                r"<input\b[^>]*"
                r"\btype\s*=\s*"
                r"""["']password["']""",
                
                body,

                re.IGNORECASE

            )


            if password_inputs:

                password_forms.append({

                    "action": action,

                    "method": method,

                    "password_inputs":
                        len(password_inputs)

                })


                if action:

                    try:

                        absolute_action = urljoin(
                            self.url,
                            action
                        )


                        form_host = (
                            urlsplit(
                                absolute_action
                            ).hostname
                            or ""
                        ).lower()


                        current_host = (
                            self.hostname
                            or ""
                        ).lower()


                        if (
                            form_host
                            and
                            form_host != current_host
                        ):

                            external_form_actions.append(
                                absolute_action
                            )


                    except Exception:

                        pass


        self.metrics["password_forms"] = (
            password_forms
        )


        self.metrics["external_form_actions"] = (
            external_form_actions
        )


        if password_forms:

            self.add_info(
                f"Password input detected in "
                f"{len(password_forms)} form(s)."
            )


        if external_form_actions:

            self.add_finding(

                "Form Destination",

                "HIGH",

                "Password form submits to another hostname",

                "A form containing a password input appears to submit to a different hostname.",

                evidence=
                    ", ".join(
                        external_form_actions
                    ),

                recommendation=
                    "Verify the form destination and ensure credentials are sent only to the intended organization.",

                score=15,

                confidence="HIGH"

            )


        # ----------------------------------------------------
        # IFRAMES
        # ----------------------------------------------------

        iframe_matches = re.findall(

            r"<iframe\b([^>]*)>",

            html,

            re.IGNORECASE

        )


        self.metrics["iframe_count"] = (
            len(iframe_matches)
        )


        external_iframes = []


        for attributes in iframe_matches:

            src_match = re.search(

                r"\bsrc\s*=\s*"
                r"""["']([^"']+)["']""",

                attributes,

                re.IGNORECASE

            )


            if not src_match:
                continue


            src = src_match.group(1).strip()


            if not src:
                continue


            try:

                iframe_url = urljoin(
                    self.url,
                    src
                )


                iframe_host = (
                    urlsplit(
                        iframe_url
                    ).hostname
                    or ""
                ).lower()


                if (
                    iframe_host
                    and
                    iframe_host != self.hostname
                ):

                    external_iframes.append(
                        iframe_url
                    )


            except Exception:

                continue


        self.metrics["external_iframes"] = (
            external_iframes
        )


        if external_iframes:

            self.add_finding(

                "HTML Structure",

                "LOW",

                "External iframe detected",

                "The page embeds content from another hostname.",

                evidence=
                    ", ".join(
                        external_iframes[:5]
                    ),

                recommendation=
                    "Review external frames and verify that they are expected.",

                score=3,

                confidence="LOW"

            )


        # ----------------------------------------------------
        # META REFRESH
        # ----------------------------------------------------

        meta_refreshes = re.findall(

            r"<meta\b[^>]*"
            r"\bhttp-equiv\s*=\s*"
            r"""["']refresh["']"""
            r"[^>]*>",

            html,

            re.IGNORECASE

        )


        self.metrics["meta_refresh_count"] = (
            len(meta_refreshes)
        )


        if meta_refreshes:

            self.add_finding(

                "HTML Redirect",

                "MEDIUM",

                "Meta refresh detected",

                "The page contains a meta refresh directive that may redirect the browser.",

                evidence=
                    f"{len(meta_refreshes)} meta refresh tag(s)",

                recommendation=
                    "Inspect the refresh destination before trusting the page.",

                score=5,

                confidence="MEDIUM"

            )


        # ----------------------------------------------------
        # JAVASCRIPT
        # ----------------------------------------------------

        script_blocks = re.findall(

            r"<script\b([^>]*)>"
            r"(.*?)"
            r"</script>",

            html,

            re.IGNORECASE
            | re.DOTALL

        )


        self.metrics["script_count"] = (
            len(script_blocks)
        )


        external_scripts = []


        suspicious_script_patterns = []


        suspicious_js_patterns = [

            r"\beval\s*\(",

            r"\batob\s*\(",

            r"\bfromCharCode\s*\(",

            r"\bunescape\s*\(",

            r"\bdocument\.write\s*\(",

            r"\bwindow\.location\b",

            r"\blocation\.href\b",

            r"\bwindow\.open\s*\(",

            r"\bnew\s+Function\s*\("

        ]


        for attributes, script_body in script_blocks:

            src_match = re.search(

                r"\bsrc\s*=\s*"
                r"""["']([^"']+)["']""",

                attributes,

                re.IGNORECASE

            )


            if src_match:

                src = src_match.group(1).strip()


                try:

                    script_url = urljoin(
                        self.url,
                        src
                    )


                    script_host = (
                        urlsplit(
                            script_url
                        ).hostname
                        or ""
                    ).lower()


                    if (
                        script_host
                        and
                        script_host != self.hostname
                    ):

                        external_scripts.append(
                            script_url
                        )


                except Exception:

                    pass


            for pattern in suspicious_js_patterns:

                try:

                    if re.search(
                        pattern,
                        script_body,
                        re.IGNORECASE
                    ):

                        suspicious_script_patterns.append(
                            pattern
                        )

                except re.error:

                    pass


        self.metrics["external_scripts"] = (
            external_scripts
        )


        self.metrics["suspicious_javascript_patterns"] = (
            sorted(
                set(
                    suspicious_script_patterns
                )
            )
        )


        if suspicious_script_patterns:

            self.add_finding(

                "JavaScript Analysis",

                "LOW",

                "Potentially obfuscated or dynamic JavaScript pattern",

                "The page contains JavaScript patterns that can be used for dynamic execution or browser redirection.",

                evidence=
                    ", ".join(
                        sorted(
                            set(
                                suspicious_script_patterns
                            )
                        )
                    ),

                recommendation=
                    "Review the JavaScript source before trusting the page.",

                score=3,

                confidence="LOW"

            )


        # ----------------------------------------------------
        # HIDDEN ELEMENTS
        # ----------------------------------------------------

        hidden_patterns = [

            r"display\s*:\s*none",

            r"visibility\s*:\s*hidden",

            r"opacity\s*:\s*0"

        ]


        hidden_count = 0


        for pattern in hidden_patterns:

            hidden_count += len(
                re.findall(
                    pattern,
                    html,
                    re.IGNORECASE
                )
            )


        self.metrics["hidden_style_matches"] = (
            hidden_count
        )


        if hidden_count >= 5:

            self.add_finding(

                "HTML Structure",

                "LOW",

                "Multiple hidden HTML elements",

                "The page contains several hidden elements.",

                evidence=
                    f"Hidden style matches: {hidden_count}",

                recommendation=
                    "Review hidden content if the page is suspected of deception.",

                score=2,

                confidence="LOW"

            )


        # ----------------------------------------------------
        # EMAIL / CREDENTIAL WORDS
        # ----------------------------------------------------

        page_text = re.sub(
            r"<script\b.*?</script>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL
        )


        page_text = re.sub(
            r"<style\b.*?</style>",
            " ",
            page_text,
            flags=re.IGNORECASE | re.DOTALL
        )


        page_text = re.sub(
            r"<[^>]+>",
            " ",
            page_text
        )


        page_text = normalize_whitespace(
            page_text
        )


        self.metrics["visible_text_length"] = (
            len(page_text)
        )


        page_lower = page_text.lower()


        page_keywords = {}


        for keyword, weight in SUSPICIOUS_KEYWORDS.items():

            if keyword in page_lower:

                page_keywords[keyword] = weight


        self.metrics["page_suspicious_keywords"] = (
            page_keywords
        )


        if len(page_keywords) >= 8:

            self.add_finding(

                "Page Content",

                "MEDIUM",

                "Many security-sensitive words on page",

                "The page contains numerous words associated with accounts, verification, authentication, payments, or urgency.",

                evidence=
                    ", ".join(
                        sorted(
                            page_keywords.keys()
                        )[:20]
                    ),

                recommendation=
                    "Verify the organization and page destination before entering information.",

                score=5,

                confidence="LOW"

            )


# ============================================================
# END OF PART 2
# ============================================================
    # ============================================================
    # RISK CALCULATION
    # ============================================================

    def calculate_risk(self):
        """
        Convert collected findings into a final risk level and synthesize
        an actionable MITRE ATT&CK & SOC Incident Response profile.
        """
        if getattr(self, "is_verified_official", False):
            self.score = 0
            self.findings = []
            risk_level = "BENIGN / VERIFIED"
            self.metrics["risk_level"] = risk_level
            self.metrics["score"] = 0
            self.ethical_hacking_profile = {
                "mitre_tactics": ["Legitimate Traffic (RFC Compliant)"],
                "mitre_techniques": [],
                "targeted_brand": None,
                "attack_vector": "Verified Official Domain",
                "soc_remediation": ["Traffic is verified benign. No SOC escalation required."]
            }
            return

        if self.score < 0:
            self.score = 0
        if self.score > 100:
            self.score = 100

        critical_count = sum(1 for f in self.findings if str(f.severity).upper() == "CRITICAL")
        high_count = sum(1 for f in self.findings if str(f.severity).upper() == "HIGH")
        medium_count = sum(1 for f in self.findings if str(f.severity).upper() == "MEDIUM")
        low_count = sum(1 for f in self.findings if str(f.severity).upper() == "LOW")

        if critical_count > 0 or self.score >= 65:
            risk_level = "CRITICAL"
        elif high_count > 0 or self.score >= 35:
            risk_level = "HIGH"
        elif medium_count >= 2 or self.score >= 20:
            risk_level = "MEDIUM"
        elif self.score >= 10 or low_count > 0:
            risk_level = "LOW"
        else:
            risk_level = "MINIMAL"

        self.metrics["risk_level"] = risk_level
        self.metrics["score"] = self.score

        # Synthesize MITRE ATT&CK Matrix
        mitre_tactics = set()
        mitre_techniques = []

        has_brand = bool(self.ethical_hacking_profile.get("targeted_brand"))
        has_creds = any("keyword" in str(f.title).lower() or "login" in str(f.evidence).lower() for f in self.findings)
        has_obfuscation = any("entropy" in str(f.title).lower() or "typosquatting" in str(f.title).lower() or "homoglyph" in str(f.title).lower() for f in self.findings)
        has_file = any("extension" in str(f.title).lower() or "executable" in str(f.title).lower() for f in self.findings)

        if has_brand or has_creds or self.score >= 30:
            mitre_tactics.add("Initial Access (TA0001)")
            mitre_techniques.append({"id": "T1566.002", "name": "Phishing: Spearphishing Link"})

        if has_obfuscation or has_brand:
            mitre_tactics.add("Defense Evasion (TA0005)")
            mitre_techniques.append({"id": "T1036.005", "name": "Masquerading: Match Legitimate Name"})

        if has_creds:
            mitre_tactics.add("Credential Access (TA0006)")
            mitre_techniques.append({"id": "T1056.003", "name": "Input Capture: Web Credential Harvesting"})

        if has_file:
            mitre_tactics.add("Execution (TA0002)")
            mitre_techniques.append({"id": "T1204.002", "name": "User Execution: Malicious File"})

        self.ethical_hacking_profile["mitre_tactics"] = sorted(list(mitre_tactics))
        self.ethical_hacking_profile["mitre_techniques"] = mitre_techniques

        # Synthesize SOC Incident Response Playbook
        soc_actions = []
        host = self.hostname or self.url
        if self.score >= 50 or critical_count > 0:
            soc_actions.append(f"DNS Sinkhole: Deploy sinkhole record for '{host}' on boundary recursive resolvers.")
            soc_actions.append(f"Perimeter Firewall: Add egress drop rule for IP/FQDN '{host}' on ports 80/443.")
            soc_actions.append("SIEM Query: Search proxy/EDR telemetry for HTTP GET/POST requests matching this URI in the past 14 days.")
            if has_creds:
                soc_actions.append("Identity Response: Force MFA credential resets for any user account that accessed this URL.")
        elif self.score >= 20:
            soc_actions.append("Passive Monitoring: Add domain to watchlist on perimeter web proxy.")
            soc_actions.append("User Awareness: Review user reported email headers if link originated from an inbound email.")
        else:
            soc_actions.append("Standard Logging: No immediate malicious indicators. Maintain standard event telemetry.")

        self.ethical_hacking_profile["soc_remediation"] = soc_actions

    def build_result(self):
        """
        Build the final result dictionary.

        This dictionary is used by the terminal report
        and JSON report.
        """

        final_url = self.url

        if self.response is not None:
            try:
                final_url = self.response.url
            except Exception:
                final_url = self.url

        result = {
            "tool": TOOL_NAME,
            "module": MODULE_NAME,
            "version": VERSION,

            "target": self.original_url,
            "normalized_url": self.url,
            "final_url": final_url,

            "risk_score": self.score,
            "risk_level": self.metrics.get(
                "risk_level",
                "UNKNOWN"
            ),

            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],

            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "info": list(self.info),

            "redirect_chain": list(
                self.redirect_chain
            ),

            "cookies": list(self.cookies),

            "metrics": dict(self.metrics),

            "analysis_started": self.start_time,
            "analysis_finished": datetime.now().isoformat(),

            "fetch_content": self.fetch_content,
            "verify_tls": self.verify_tls,
            "timeout": self.timeout,
        }

        result["is_verified_official"] = getattr(self, "is_verified_official", False)
        result["ethical_hacking_profile"] = getattr(self, "ethical_hacking_profile", {})
        return result

    # ============================================================
    # MAIN ANALYSIS ENGINE
    # ============================================================

    def analyze(self):
        """
        Run the complete phishing URL analysis.

        Order:

        1. Normalize URL
        2. URL-layer analysis
        3. Optional HTTP request
        4. Page analysis
        5. Risk calculation
        6. Build final result
        """

        self.start_time = datetime.now().isoformat()

        # --------------------------------------------------------
        # STEP 1 - Normalize URL
        # --------------------------------------------------------

        normalized = self.normalize_url()

        if not normalized:
            self.calculate_risk()
            return self.build_result()

        # --------------------------------------------------------
        # STEP 2 - URL analysis
        # --------------------------------------------------------

        try:
            self.scan_url_layer()

        except Exception as error:
            self.add_error(
                f"URL analysis failed: {error}"
            )

        # --------------------------------------------------------
        # STEP 3 - HTTP / page analysis
        # --------------------------------------------------------

        if self.fetch_content:

            try:
                self.fetch_page()

            except Exception as error:
                self.add_error(
                    f"Page analysis failed: {error}"
                )

        # --------------------------------------------------------
        # STEP 4 - Final risk calculation
        # --------------------------------------------------------

        try:
            self.calculate_risk()

        except Exception as error:
            self.add_error(
                f"Risk calculation failed: {error}"
            )

        # --------------------------------------------------------
        # STEP 5 - Build result
        # --------------------------------------------------------

        return self.build_result()


# =================================================================
# TERMINAL UI
# =================================================================


def print_banner():
    """
    Display NIGHT HUNTER phishing analyzer banner.
    """

    print()
    print(
        BLUE
        + "============================================================"
        + RESET
    )

    print(
        RED
        + "                    NIGHT HUNTER"
        + RESET
    )

    print(
        CYAN
        + "                 PHISHING URL ANALYZER"
        + RESET
    )

    print(
        BLUE
        + "============================================================"
        + RESET
    )

    print(
        GRAY
        + "Defensive URL and webpage security analysis"
        + RESET
    )

    print()


def severity_color(severity):
    """
    Return terminal color according to finding severity.
    """

    severity = str(severity).upper()

    if severity == "CRITICAL":
        return RED

    if severity == "HIGH":
        return RED

    if severity == "MEDIUM":
        return YELLOW

    if severity == "LOW":
        return CYAN

    if severity == "INFO":
        return GRAY

    return RESET


def risk_color(risk_level):
    """
    Return terminal color for overall risk.
    """

    risk_level = str(risk_level).upper()

    if risk_level == "CRITICAL":
        return RED

    if risk_level == "HIGH":
        return RED

    if risk_level == "MEDIUM":
        return YELLOW

    if risk_level == "LOW":
        return CYAN

    return GREEN


def print_section(title):
    """
    Print a clean terminal section.
    """

    print()
    print(
        BLUE
        + "------------------------------------------------------------"
        + RESET
    )

    print(
        CYAN
        + f" {title}"
        + RESET
    )

    print(
        BLUE
        + "------------------------------------------------------------"
        + RESET
    )


def print_report(result):
    """
    Print complete analysis result.
    """

    print()

    print_section("ANALYSIS SUMMARY")

    print(
        f"{WHITE}Target:{RESET} "
        f"{result.get('target', 'Unknown')}"
    )

    print(
        f"{WHITE}Normalized URL:{RESET} "
        f"{result.get('normalized_url', 'Unknown')}"
    )

    print(
        f"{WHITE}Final URL:{RESET} "
        f"{result.get('final_url', 'Unknown')}"
    )

    score = result.get("risk_score", 0)
    level = result.get("risk_level", "UNKNOWN")

    print(
        f"{WHITE}Risk Score:{RESET} "
        f"{score}/100"
    )

    print(
        f"{WHITE}Risk Level:{RESET} "
        f"{risk_color(level)}{level}{RESET}"
    )

    print_section("FINDING COUNTS")

    metrics = result.get("metrics", {})

    print(
        f"{WHITE}Total Findings:{RESET} "
        f"{metrics.get('total_findings', 0)}"
    )

    print(
        f"{WHITE}Critical:{RESET} "
        f"{metrics.get('critical_findings', 0)}"
    )

    print(
        f"{WHITE}High:{RESET} "
        f"{metrics.get('high_findings', 0)}"
    )

    print(
        f"{WHITE}Medium:{RESET} "
        f"{metrics.get('medium_findings', 0)}"
    )

    print(
        f"{WHITE}Low:{RESET} "
        f"{metrics.get('low_findings', 0)}"
    )

    print(
        f"{WHITE}Info:{RESET} "
        f"{metrics.get('info_findings', 0)}"
    )

    print(
        f"{WHITE}Warnings:{RESET} "
        f"{metrics.get('total_warnings', 0)}"
    )

    print(
        f"{WHITE}Errors:{RESET} "
        f"{metrics.get('total_errors', 0)}"
    )

    # ------------------------------------------------------------
    # Findings
    # ------------------------------------------------------------

    print_section("SECURITY FINDINGS")

    findings = result.get("findings", [])

    if not findings:

        print(
            GREEN
            + "[+] No security findings were generated."
            + RESET
        )

    else:

        for index, finding in enumerate(
            findings,
            start=1
        ):

            severity = finding.get(
                "severity",
                "INFO"
            )

            color = severity_color(
                severity
            )

            print()

            print(
                f"{WHITE}[{index}] "
                f"{color}{severity}{RESET}"
            )

            print(
                f"    Category: "
                f"{finding.get('category', 'Unknown')}"
            )

            print(
                f"    Title: "
                f"{finding.get('title', 'Unknown')}"
            )

            print(
                f"    Description: "
                f"{finding.get('description', '')}"
            )

            evidence = finding.get(
                "evidence",
                ""
            )

            if evidence:

                print(
                    f"    Evidence: "
                    f"{evidence}"
                )

            recommendation = finding.get(
                "recommendation",
                ""
            )

            if recommendation:

                print(
                    f"    Recommendation: "
                    f"{recommendation}"
                )

    # ------------------------------------------------------------
    # Redirect chain
    # ------------------------------------------------------------

    redirect_chain = result.get(
        "redirect_chain",
        []
    )

    if redirect_chain:

        print_section("REDIRECT CHAIN")

        for index, item in enumerate(
            redirect_chain,
            start=1
        ):

            print(
                f"{index}. {item}"
            )

    # ------------------------------------------------------------
    # Warnings
    # ------------------------------------------------------------

    warnings = result.get(
        "warnings",
        []
    )

    if warnings:

        print_section("WARNINGS")

        for warning in warnings:

            print(
                YELLOW
                + f"[!] {warning}"
                + RESET
            )

    # ------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------

    errors = result.get(
        "errors",
        []
    )

    if errors:

        print_section("ERRORS")

        for error in errors:

            print(
                RED
                + f"[!] {error}"
                + RESET
            )

    # ------------------------------------------------------------
    # Informational messages
    # ------------------------------------------------------------

    info = result.get(
        "info",
        []
    )

    if info:

        print_section("INFORMATION")

        for item in info:

            print(
                f"[*] {item}"
            )

    print()

    print(
        BLUE
        + "============================================================"
        + RESET
    )

    print(
        GREEN
        + "                ANALYSIS COMPLETED"
        + RESET
    )

    print(
        BLUE
        + "============================================================"
        + RESET
    )

    print()


# =================================================================
# JSON REPORT
# =================================================================


def save_json_report(result, filename=None):
    """
    Save analysis result as JSON.

    If no filename is supplied, a timestamped filename
    is generated automatically.
    """

    if filename is None:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"night_hunter_phishing_{timestamp}.json"
        )

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            GREEN
            + f"[+] JSON report saved: {filename}"
            + RESET
        )

        return filename

    except Exception as error:

        print(
            RED
            + f"[!] Unable to save report: {error}"
            + RESET
        )

        return None


# =================================================================
# INTERACTIVE MODE
# =================================================================
def interactive_mode():

    while True:

        print()

        print(
            CYAN
            + "============================================================"
            + RESET
        )

        print(
            WHITE
            + "                 PHISHING ANALYZER"
            + RESET
        )

        print(
            CYAN
            + "============================================================"
            + RESET
        )

        print()

        print(
            f"{WHITE}[1]{RESET} Analyze URL"
        )

        print(
            f"{WHITE}[2]{RESET} Analyze URL without HTTP request"
        )

        print(
            f"{WHITE}[3]{RESET} Exit"
        )

        print()

        choice = input(
            "Select option: "
        ).strip()

        # ========================================================
        # OPTION 1 - FULL URL + WEBPAGE ANALYSIS
        # ========================================================

        if choice == "1":

            print()

            target = input(
                "Enter URL: "
            ).strip()

            # Prevent accidental PowerShell commands
            if (
                target.startswith("python ")
                or target.startswith("python3 ")
                or target.startswith("py ")
                or target.startswith("& ")
            ):

                print()

                print(
                    YELLOW
                    + "[!] You entered a terminal command, not a URL."
                    + RESET
                )

                print(
                    CYAN
                    + "[*] Example: https://itvedant.com"
                    + RESET
                )

                print()

                continue

            if not target:

                print()

                print(
                    RED
                    + "[!] URL cannot be empty."
                    + RESET
                )

                continue

            print()

            print(
                CYAN
                + "[*] Starting analysis..."
                + RESET
            )

            print()

            analyzer = PhishingAnalyzer(
                target,
                fetch_content=True
            )

            result = analyzer.analyze()

            print_report(
                result
            )

            print()

            save = input(
                "Save JSON report? [y/N]: "
            ).strip().lower()

            if save == "y":

                filename = input(
                    "Enter filename: "
                ).strip()

                if not filename:

                    filename = (
                        "phishing_report.json"
                    )

                if save_json_report(
                    result,
                    filename
                ):

                    print()

                    print(
                        GREEN
                        + "Report saved."
                        + RESET
                    )

        # ========================================================
        # OPTION 2 - URL-ONLY ANALYSIS
        # ========================================================

        elif choice == "2":

            print()

            target = input(
                "Enter URL: "
            ).strip()

            # Prevent accidental PowerShell commands
            if (
                target.startswith("python ")
                or target.startswith("python3 ")
                or target.startswith("py ")
                or target.startswith("& ")
            ):

                print()

                print(
                    YELLOW
                    + "[!] You entered a terminal command, not a URL."
                    + RESET
                )

                print(
                    CYAN
                    + "[*] Example: https://itvedant.com"
                    + RESET
                )

                print()

                continue

            if not target:

                print()

                print(
                    RED
                    + "[!] URL cannot be empty."
                    + RESET
                )

                continue

            print()

            print(
                CYAN
                + "[*] Running URL-only analysis..."
                + RESET
            )

            print()

            analyzer = PhishingAnalyzer(
                target,
                fetch_content=False
            )

            result = analyzer.analyze()

            print_report(
                result
            )

            print()

            save = input(
                "Save JSON report? [y/N]: "
            ).strip().lower()

            if save == "y":

                filename = input(
                    "Enter filename: "
                ).strip()

                if not filename:

                    filename = (
                        "phishing_report.json"
                    )

                if save_json_report(
                    result,
                    filename
                ):

                    print()

                    print(
                        GREEN
                        + "Report saved."
                        + RESET
                    )

        # ========================================================
        # OPTION 3 - EXIT
        # ========================================================

        elif choice == "3":

            print()

            print(
                GREEN
                + "[+] Exiting NIGHT HUNTER."
                + RESET
            )

            print()

            break

        # ========================================================
        # INVALID OPTION
        # ========================================================

        else:

            print()

            print(
                YELLOW
                + "[!] Invalid option."
                + RESET
            )

            print(
                GRAY
                + "[*] Please select 1, 2, or 3."
                + RESET
            )



# =================================================================
# COMMAND LINE MODE
# =================================================================


def command_line_mode():
    """
    Command-line interface.

    Examples:

        python url_analyzer.py --url https://example.com

        python url_analyzer.py \
            --url https://example.com \
            --no-fetch

        python url_analyzer.py \
            --url https://example.com \
            --json report.json
    """

    parser = argparse.ArgumentParser(
        description=(
            "NIGHT HUNTER - Phishing URL Analyzer"
        )
    )

    parser.add_argument(
        "--url",
        help="URL to analyze"
    )

    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help=(
            "Perform URL analysis without "
            "making an HTTP request"
        )
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP timeout in seconds"
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help=(
            "Disable TLS certificate verification"
        )
    )

    parser.add_argument(
        "--json",
        nargs="?",
        const="",
        help=(
            "Save JSON report. "
            "Optional filename can be supplied."
        )
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help=(
            "Reduce terminal output"
        )
    )

    args = parser.parse_args()

    # ------------------------------------------------------------
    # If no URL is supplied, open interactive mode.
    # ------------------------------------------------------------

    if not args.url:

        print_banner()

        interactive_mode()

        return

    # ------------------------------------------------------------
    # Create analyzer
    # ------------------------------------------------------------

    analyzer = PhishingAnalyzer(
        args.url,
        timeout=args.timeout,
        fetch_content=not args.no_fetch,
        verify_tls=not args.insecure
    )

    # ------------------------------------------------------------
    # Run analysis
    # ------------------------------------------------------------

    result = analyzer.analyze()

    # ------------------------------------------------------------
    # Terminal output
    # ------------------------------------------------------------

    if not args.quiet:

        print_banner()

        print_report(result)

    # ------------------------------------------------------------
    # JSON output
    # ------------------------------------------------------------

    if args.json is not None:

        filename = args.json

        if not filename:

            filename = None

        save_json_report(
            result,
            filename
        )


# =================================================================
# PROGRAM ENTRY POINT
# =================================================================


if __name__ == "__main__":

    try:

        command_line_mode()

    except KeyboardInterrupt:

        print()

        print(
            YELLOW
            + "[!] Analysis interrupted by user."
            + RESET
        )

    except Exception as error:

        print()

        print(
            RED
            + "[!] NIGHT HUNTER encountered an unexpected error."
            + RESET
        )

        print(
            RED
            + f"[!] {error}"
            + RESET
        )