# NIGHT HUNTER - Network Security Integration

import sys
from pathlib import Path


# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# IMPORT NETWORK MODULES
# ---------------------------------------------------------

from modules.network_security import checker
from modules.network_security import pentest
from modules.network_security import load_benchmark


# ---------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------

def show_banner():
    print()
    print("=" * 64)
    print("NIGHT HUNTER - NETWORK SECURITY")
    print("=" * 64)


def show_menu():
    print()
    print("-" * 64)
    print("[1] Network Security Check")
    print("[2] Network Pentest")
    print("[3] HTTP Availability & Latency Benchmark")
    print("[4] Network Information")
    print("[0] Back / Exit")
    print("-" * 64)


# ---------------------------------------------------------
# NETWORK SECURITY CHECK
# ---------------------------------------------------------

def run_security_check():
    print()
    print("=" * 64)
    print("NETWORK SECURITY CHECK")
    print("=" * 64)

    host = input("Enter host or IP: ").strip()

    if not host:
        print("[!] Host cannot be empty.")
        return

    try:
        result = checker.run_network_check(host)

        if result is None:
            print()
            print("[!] Network check returned no result.")
            return

        print()
        print("=" * 64)
        print("NETWORK CHECK COMPLETED")
        print("=" * 64)

        if isinstance(result, dict):

            for key, value in result.items():

                if isinstance(value, list):
                    print()
                    print(f"{key}:")
                    for item in value:
                        print(f"  {item}")

                elif isinstance(value, dict):
                    print()
                    print(f"{key}:")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")

                else:
                    print(f"{key}: {value}")

        else:
            print(result)

    except Exception as error:
        print()
        print(f"[!] Network security check failed: {error}")


# ---------------------------------------------------------
# NETWORK PENTEST
# ---------------------------------------------------------

def run_pentest():
    print()
    print("=" * 64)
    print("NETWORK PENTEST")
    print("=" * 64)

    host = input("Enter authorized target host/IP: ").strip()

    if not host:
        print("[!] Host cannot be empty.")
        return

    print()
    print("[*] Starting network pentest...")
    print("[*] Use only on systems you own or are authorized to test.")
    print()

    try:

        if hasattr(pentest, "run_network_pentest"):

            result = pentest.run_network_pentest(host)

        elif hasattr(pentest, "network_pentest"):

            result = pentest.network_pentest(host)

        elif hasattr(pentest, "run_pentest"):

            result = pentest.run_pentest(host)

        else:

            print("[!] Could not find the pentest entry function.")
            print("[!] Check modules/network_security/pentest.py")
            return

        print()
        print("=" * 64)
        print("NETWORK PENTEST COMPLETED")
        print("=" * 64)

        if isinstance(result, dict):

            for key, value in result.items():

                if isinstance(value, list):
                    print()
                    print(f"{key}:")
                    for item in value:
                        print(f"  {item}")

                elif isinstance(value, dict):
                    print()
                    print(f"{key}:")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")

                else:
                    print(f"{key}: {value}")

        else:
            print(result)

    except Exception as error:
        print()
        print(f"[!] Network pentest failed: {error}")


# ---------------------------------------------------------
# NETWORK INFORMATION
# ---------------------------------------------------------

def show_network_information():

    print()
    print("=" * 64)
    print("NIGHT HUNTER - NETWORK DEVICE INFORMATION & RECON")
    print("=" * 64)
    print()
    print("[!] CAUTION: For local device name, MAC address, and OS model detection,")
    print("    the target device should be connected to the SAME local network (LAN / Wi-Fi).")
    print()

    target = input("Enter target device IP address (e.g., 192.168.1.15) [default: 127.0.0.1]: ").strip()
    if not target:
        target = "127.0.0.1"

    print(f"\n[*] Scanning target device {target} (Nmap recon + OS & TCP/UDP port scan)...")

    try:
        if hasattr(checker, "get_device_recon"):
            info = checker.get_device_recon(target)
        elif hasattr(checker, "get_network_info"):
            info = checker.get_network_info(target)
        else:
            print("[!] Device recon function not found.")
            return

        if not info:
            print("[!] No information returned for target.")
            return

        print()
        print("=" * 64)
        print("TARGET DEVICE INTELLIGENCE")
        print("=" * 64)
        print(f"Target IP       : {info.get('ip_address', target)}")
        print(f"Device Name     : {info.get('device_name', 'Unknown')}")
        print(f"OS Model        : {info.get('os_model', 'Unknown OS')}")
        print(f"Device Type     : {info.get('device_type', 'general purpose')}")
        if info.get('mac_address'):
            vendor_str = f" ({info.get('mac_vendor')})" if info.get('mac_vendor') else ""
            print(f"MAC Address     : {info.get('mac_address')}{vendor_str}")
        print(f"Scan Engine     : {info.get('scan_engine', 'Nmap')}")
        print(f"Scan Timestamp  : {info.get('timestamp')}")
        print("=" * 64)

        tcp_ports = info.get('tcp_ports', [])
        print(f"\n[+] OPEN TCP PORTS ({len(tcp_ports)} found):")
        if tcp_ports:
            print(f"    {'PORT':<8} {'SERVICE':<18} {'STATE':<10}")
            print("    " + "-" * 38)
            for p in tcp_ports:
                print(f"    {p.get('port', ''):<8} {p.get('service', 'unknown'):<18} {p.get('state', 'OPEN'):<10}")
        else:
            print("    No open TCP ports found.")

        udp_ports = info.get('udp_ports', [])
        print(f"\n[+] OPEN UDP PORTS - Nmap -sU ({len(udp_ports)} found):")
        if udp_ports:
            print(f"    {'PORT':<8} {'SERVICE':<18} {'STATE':<14}")
            print("    " + "-" * 42)
            for p in udp_ports:
                print(f"    {p.get('port', ''):<8} {p.get('service', 'unknown'):<18} {p.get('state', 'OPEN'):<14}")
        else:
            print("    No open UDP ports found.")
        print("=" * 64)

    except Exception as error:
        print()
        print(f"[!] Unable to collect device information: {error}")


# ---------------------------------------------------------
# CONTROLLED STRESS TEST
# ---------------------------------------------------------

def run_stress_test():

    print()
    print("=" * 64)
    print("CONTROLLED HTTP STRESS TEST")
    print("=" * 64)

    print()
    print("[!] Authorized testing only.")
    print("[!] This module is intended for controlled load testing.")
    print()

    target = input("Enter authorized HTTP/HTTPS URL: ").strip()

    if not target:
        print("[!] URL cannot be empty.")
        return

    try:
        workers_input = input(
            "Workers [default 5]: "
        ).strip()

        duration_input = input(
            "Duration in seconds [default 10]: "
        ).strip()

        workers = int(workers_input) if workers_input else 5
        duration = int(duration_input) if duration_input else 10

        if workers < 1:
            print("[!] Workers must be at least 1.")
            return

        if duration < 1:
            print("[!] Duration must be at least 1 second.")
            return

        if workers > 20:
            print("[!] Workers cannot exceed 20.")
            return

        if duration > 300:
            print("[!] Duration cannot exceed 300 seconds.")
            return

        print()
        print("[*] Starting HTTP latency and availability benchmark...")
        print()

        if hasattr(load_benchmark, "run_load_benchmark"):
            result = load_benchmark.run_load_benchmark(
                target,
                duration=duration,
                workers=workers
            )
        elif hasattr(load_benchmark, "run_stress_test"):
            result = load_benchmark.run_stress_test(
                target,
                duration=duration,
                workers=workers
            )
        else:
            print("[!] Could not find benchmark entry function.")
            print("[!] Check modules/network_security/load_benchmark.py")
            return

        print()
        print("=" * 64)
        print("HTTP BENCHMARK COMPLETED")
        print("=" * 64)

        if result is not None:
            print(result)

    except ValueError:
        print("[!] Workers and duration must be numbers.")

    except Exception as error:
        print()
        print(f"[!] Stress test failed: {error}")


# ---------------------------------------------------------
# MAIN INTEGRATION MENU
# ---------------------------------------------------------

def main():

    while True:

        show_banner()
        show_menu()

        choice = input("Enter choice: ").strip()

        if choice == "1":

            run_security_check()

        elif choice == "2":

            run_pentest()

        elif choice == "3":

            run_stress_test()

        elif choice == "4":

            show_network_information()

        elif choice == "0":

            print()
            print("Returning from Network Security module...")
            break

        else:

            print()
            print("[!] Invalid choice.")

        input("\nPress Enter to continue...")


# ---------------------------------------------------------
# DIRECT EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
    