import sys

from pathlib import Path

from urllib.parse import urlparse

# ============================================================

# PROJECT PATH

# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================

# URL NORMALIZER

# ============================================================

def normalize_url(url):

    url = url.strip()

    if not url:

        return ""

    if not url.startswith(("http://", "https://")):

        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:

        return ""

    return url

# ============================================================

# WEB SECURITY

# ============================================================

def run_web_security():

    try:

        from modules.web_security.pentest import run_web_pentest

        print()

        print("[*] Web Security")

        print()

        url = input("Target URL > ").strip()

        if not url:

            print()

            print("[!] URL cannot be empty.")

            input("\nPress Enter to continue...")

            return

        url = normalize_url(url)

        if not url:

            print()

            print("[!] Invalid URL.")

            input("\nPress Enter to continue...")

            return

        print()

        print("[*] Starting Web Security Pentest...")

        print()

        run_web_pentest(url)

    except Exception as error:

        print()

        print("[!] Web Security error:")

        print(error)

    input("\nPress Enter to return to Night Hunter...")

# ============================================================

# PASSWORD SECURITY

# ============================================================

def run_password_security():

    try:

        from modules.password_security import checker

        print()

        print("[*] Password Security")

        print()

        print("Enter a password to check its strength.")

        print()

        password = input("Password > ")

        if not password:

            print()

            print("[!] Password cannot be empty.")

            input("\nPress Enter to continue...")

            return

        print()

        print("[*] Analyzing password...")

        print()

        result = checker.analyze_password(password)

        print()

        print("========== PASSWORD RESULT ==========")

        if isinstance(result, dict):

            for key, value in result.items():

                print(f"{key}: {value}")

        else:

            print(result)

        print("=====================================")

    except Exception as error:

        print()

        print("[!] Password Security error:")

        print(error)

    input("\nPress Enter to return to Night Hunter...")

# ============================================================

# NETWORK SECURITY

# ============================================================

def run_network_security():

    try:

        from modules.network_security.integration import main as network_main

        print()

        print("[*] Network Security")

        print()

        network_main()

    except Exception as error:

        print()

        print("[!] Network Security error:")

        print(error)

    input("\nPress Enter to return to Night Hunter...")

# ============================================================

# PHISHING

# ============================================================

def run_phishing():

    try:

        from modules.phishing.url_analyzer import interactive_mode

        print()

        print("[*] Phishing URL Analyzer")

        print()

        interactive_mode()

    except Exception as error:

        print()

        print("[!] Phishing error:")

        print(error)

    input("\nPress Enter to return to Night Hunter...")

# ============================================================

# CRYPTOGRAPHY

# ============================================================

def run_cryptography():

    try:

        from modules.cryptography.crypto_tools import interactive_mode

        print()

        print("[*] Cryptography")

        print()

        interactive_mode()

    except Exception as error:

        print()

        print("[!] Cryptography error:")

        print(error)

    input("\nPress Enter to return to Night Hunter...")

# ============================================================

# REPORTS

# ============================================================

def run_reports():

    try:

        from modules.reports.report_exporter import (

            create_test_report,

            export_all

        )

        print()

        print("[*] Reports")

        print()

        print("[1] Create Test Report")

        print("[0] Back")

        print()

        choice = input("Report > ").strip()

        if choice == "0":

            return

        if choice != "1":

            print()

            print("[!] Invalid option.")

            input("\nPress Enter to continue...")

            return

        print()

        print("[*] Creating test report...")

        print()

        test_report = create_test_report()

        results = export_all(

            test_report,

            "night_hunter_test"

        )

        print()

        print("========== REPORT FILES ==========")

        for report_type, path in results.items():

            print(

                f"{report_type.upper():6} : {path}"

            )

        print("==================================")

    except Exception as error:

        print()

        print("[!] Reports error:")

        print(error)

    input("\nPress Enter to return to Night Hunter...")

# ============================================================

# WEB DASHBOARD LAUNCHER

# ============================================================

def launch_web_dashboard():

    """Start local defensive security web server and launch default browser."""

    import os

    import threading

    import webbrowser

    from api.server import app

    host = "127.0.0.1"

    port = int(os.environ.get("NIGHT_HUNTER_PORT", "5000"))

    url = f"http://{host}:{port}/app"

    print()

    print("=" * 65)

    print("           🦇 NIGHT HUNTER v1.7.0 · DEFENSIVE OPS")

    print("=" * 65)

    print(f"[+] Local Web Dashboard : {url}")

    print("[+] Launching web browser...")

    print("[+] Web Scanner         : Domain & technology intelligence ready")

    print("[+] Phishing Station    : Homoglyph lab & email triage ready")

    print("[+] Crypto Analyst      : Format identifier & 10+ hashes ready")

    print("[+] Network Monitor     : Speed, strength & connectivity diagnostics ready")

    print()

    print("[*] Server active! Press CTRL+C to stop.")

    print("=" * 65)

    print()

    def open_browser():

        try:

            webbrowser.open_new(url)

        except Exception:

            pass

    threading.Timer(1.0, open_browser).start()

    try:

        from waitress import serve

        serve(app, host=host, port=port)

    except ImportError:

        app.run(host=host, port=port, debug=False)

# ============================================================

# TERMINAL CLI MENU

# ============================================================

def run_cli_menu():

    """Terminal interactive CLI mode for headless or shell environments."""

    from utils.banner import show_banner

    while True:

        print()

        show_banner()

        print("          NIGHT HUNTER v1.7.0 · DEFENSIVE SECURITY OPS")

        print("     Official Site: https://night-hunter-0br7.onrender.com")

        print("     Local Web App: http://127.0.0.1:5000/app")

        print()

        print("[W] Launch Graphical Web Dashboard in Browser")

        print("[1] Web Security (Domain & Technology Intelligence)")

        print("[2] Password Security Audit")

        print("[3] Network Security (Speed, Latency & Connectivity)")

        print("[4] Phishing Intelligence (Heuristics & Link Triage)")

        print("[5] Cryptography (Multi-Hash & Format Analysis)")

        print("[6] Security Reports Engine")

        print("[0] Exit")

        print()

        choice = input("NH > ").strip().upper()

        if choice == "W":

            launch_web_dashboard()

            break

        elif choice == "1":

            run_web_security()

        elif choice == "2":

            run_password_security()

        elif choice == "3":

            run_network_security()

        elif choice == "4":

            run_phishing()

        elif choice == "5":

            run_cryptography()

        elif choice == "6":

            run_reports()

        elif choice == "0":

            print("\nExiting NIGHT HUNTER...\n")

            break

        else:

            print("\n[!] Invalid option. Please select a valid menu option.")

            input("\nPress Enter to continue...")

# ============================================================

# START NIGHT HUNTER

# ============================================================

def main():

    if "--help" in sys.argv or "-h" in sys.argv:

        print("Night Hunter v1.7.0 - Defensive Security Platform")

        print("Usage:")

        print("  NightHunter           Launch full Graphical Web Dashboard in browser (Default)")

        print("  NightHunter --web     Launch full Graphical Web Dashboard in browser")

        print("  NightHunter --cli     Launch terminal command-line interface")

        print("  NightHunter --help    Show this help message")

        return

    if "--cli" in sys.argv or "-c" in sys.argv:

        run_cli_menu()

    else:

        launch_web_dashboard()

if __name__ == "__main__":

    main()

