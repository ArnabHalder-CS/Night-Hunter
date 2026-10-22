# NIGHT HUNTER - File Integrity Checker

import sys
import hashlib
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------
# PROJECT ROOT SUPPORT
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


try:
    from core.logger import log_info, log_warning, log_error
except ImportError:

    def log_info(message):
        print(f"[INFO] {message}")

    def log_warning(message):
        print(f"[WARNING] {message}")

    def log_error(message):
        print(f"[ERROR] {message}")


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

SUPPORTED_ALGORITHMS = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_256",
    "sha3_512",
    "blake2b",
    "blake2s"
]

DEFAULT_ALGORITHM = "sha256"
CHUNK_SIZE = 1024 * 1024


# ---------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------

def normalize_algorithm(algorithm):
    """
    Convert different algorithm names into hashlib names.
    """

    if not algorithm:
        return DEFAULT_ALGORITHM

    algorithm = algorithm.lower().strip()

    aliases = {
        "sha-256": "sha256",
        "sha-512": "sha512",
        "sha-1": "sha1",
        "sha-224": "sha224",
        "sha-384": "sha384",
        "sha3-256": "sha3_256",
        "sha3-512": "sha3_512",
        "blake2-b": "blake2b",
        "blake2-s": "blake2s"
    }

    return aliases.get(algorithm, algorithm)


def is_supported_algorithm(algorithm):
    """
    Check whether the selected hashing algorithm is supported.
    """

    algorithm = normalize_algorithm(algorithm)

    return algorithm in SUPPORTED_ALGORITHMS


def validate_file(file_path):
    """
    Check whether a file exists and is actually a file.
    """

    path = Path(file_path)

    if not path.exists():
        log_error(f"File does not exist: {path}")
        return False

    if not path.is_file():
        log_error(f"Path is not a file: {path}")
        return False

    return True


# ---------------------------------------------------------
# FILE INFORMATION
# ---------------------------------------------------------

def get_file_information(file_path):
    """
    Collect basic information about a file.
    """

    path = Path(file_path)

    if not validate_file(path):
        return {}

    try:
        stat = path.stat()

        information = {
            "name": path.name,
            "path": str(path.resolve()),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        return information

    except OSError as error:
        log_error(f"Unable to read file information: {error}")
        return {}


def display_file_information(file_path):
    """
    Display basic file information.
    """

    information = get_file_information(file_path)

    if not information:
        return False

    print()
    print("=" * 60)
    print("FILE INFORMATION")
    print("=" * 60)
    print(f"Name     : {information['name']}")
    print(f"Path     : {information['path']}")
    print(f"Size     : {information['size']} bytes")
    print(f"Modified : {information['modified']}")
    print("=" * 60)

    return True


# ---------------------------------------------------------
# FILE HASHING
# ---------------------------------------------------------

def calculate_file_hash(file_path, algorithm=DEFAULT_ALGORITHM):
    """
    Calculate the cryptographic hash of a file.
    """

    algorithm = normalize_algorithm(algorithm)

    if not is_supported_algorithm(algorithm):
        log_error(f"Unsupported algorithm: {algorithm}")
        return None

    if not validate_file(file_path):
        return None

    try:
        hash_object = hashlib.new(algorithm)

        with open(file_path, "rb") as file:
            while True:
                data = file.read(CHUNK_SIZE)

                if not data:
                    break

                hash_object.update(data)

        file_hash = hash_object.hexdigest()

        log_info(
            f"{algorithm.upper()} hash calculated for: {file_path}"
        )

        return file_hash

    except OSError as error:
        log_error(f"Unable to read file: {error}")
        return None

    except Exception as error:
        log_error(f"Hash calculation failed: {error}")
        return None


# ---------------------------------------------------------
# CALCULATE MULTIPLE HASHES
# ---------------------------------------------------------

def calculate_multiple_hashes(file_path):
    """
    Calculate several hashes for the same file.
    """

    if not validate_file(file_path):
        return {}

    results = {}

    for algorithm in SUPPORTED_ALGORITHMS:
        file_hash = calculate_file_hash(file_path, algorithm)

        if file_hash:
            results[algorithm] = file_hash

    return results


def display_multiple_hashes(file_path):
    """
    Display multiple file hashes.
    """

    results = calculate_multiple_hashes(file_path)

    if not results:
        return False

    print()
    print("=" * 60)
    print("FILE HASHES")
    print("=" * 60)

    for algorithm, file_hash in results.items():
        print()
        print(f"{algorithm.upper()}:")
        print(file_hash)

    print("=" * 60)

    return True


# ---------------------------------------------------------
# HASH COMPARISON
# ---------------------------------------------------------

def compare_file_hash(
    file_path,
    expected_hash,
    algorithm=DEFAULT_ALGORITHM
):
    """
    Compare the current file hash with an expected hash.
    """

    algorithm = normalize_algorithm(algorithm)

    if not expected_hash:
        log_error("Expected hash cannot be empty.")
        return False

    current_hash = calculate_file_hash(
        file_path,
        algorithm
    )

    if not current_hash:
        return False

    expected_hash = expected_hash.strip().lower()

    print()
    print("=" * 60)
    print("HASH COMPARISON")
    print("=" * 60)
    print(f"Algorithm    : {algorithm.upper()}")
    print(f"Expected Hash: {expected_hash}")
    print(f"Current Hash : {current_hash}")
    print("=" * 60)

    if current_hash.lower() == expected_hash:
        print("[+] HASH MATCH")
        print("[+] File integrity appears unchanged.")
        return True

    print("[-] HASH MISMATCH")
    print("[-] File contents may have changed.")

    return False


# ---------------------------------------------------------
# FILE-TO-FILE COMPARISON
# ---------------------------------------------------------

def compare_two_files(
    first_file,
    second_file,
    algorithm=DEFAULT_ALGORITHM
):
    """
    Compare two files using their hashes.
    """

    algorithm = normalize_algorithm(algorithm)

    if not validate_file(first_file):
        return False

    if not validate_file(second_file):
        return False

    first_hash = calculate_file_hash(
        first_file,
        algorithm
    )

    second_hash = calculate_file_hash(
        second_file,
        algorithm
    )

    if not first_hash or not second_hash:
        return False

    print()
    print("=" * 60)
    print("FILE COMPARISON")
    print("=" * 60)
    print(f"Algorithm : {algorithm.upper()}")
    print()
    print(f"File 1:")
    print(first_file)
    print(first_hash)
    print()
    print(f"File 2:")
    print(second_file)
    print(second_hash)
    print("=" * 60)

    if first_hash == second_hash:
        print("[+] FILES MATCH")
        print("[+] Both files have the same hash.")
        return True

    print("[-] FILES DIFFER")
    print("[-] The files do not have the same hash.")

    return False


# ---------------------------------------------------------
# INTEGRITY RECORD
# ---------------------------------------------------------

def create_integrity_record(
    file_path,
    algorithm=DEFAULT_ALGORITHM
):
    """
    Create a simple integrity record for a file.
    """

    algorithm = normalize_algorithm(algorithm)

    file_hash = calculate_file_hash(
        file_path,
        algorithm
    )

    if not file_hash:
        return None

    information = get_file_information(file_path)

    if not information:
        return None

    record = {
        "file": information["name"],
        "path": information["path"],
        "size": information["size"],
        "modified": information["modified"],
        "algorithm": algorithm,
        "hash": file_hash,
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    return record


def display_integrity_record(
    file_path,
    algorithm=DEFAULT_ALGORITHM
):
    """
    Display an integrity record.
    """

    record = create_integrity_record(
        file_path,
        algorithm
    )

    if not record:
        return False

    print()
    print("=" * 60)
    print("FILE INTEGRITY RECORD")
    print("=" * 60)
    print(f"File      : {record['file']}")
    print(f"Path      : {record['path']}")
    print(f"Size      : {record['size']} bytes")
    print(f"Modified  : {record['modified']}")
    print(f"Algorithm : {record['algorithm'].upper()}")
    print(f"Hash      : {record['hash']}")
    print(f"Created   : {record['created']}")
    print("=" * 60)

    return True


# ---------------------------------------------------------
# VERIFY INTEGRITY RECORD
# ---------------------------------------------------------

def verify_integrity_record(record):
    """
    Verify a file using a previously created integrity record.
    """

    if not isinstance(record, dict):
        log_error("Invalid integrity record.")
        return False

    file_path = record.get("path")
    expected_hash = record.get("hash")
    algorithm = record.get(
        "algorithm",
        DEFAULT_ALGORITHM
    )

    if not file_path:
        log_error("Integrity record does not contain a file path.")
        return False

    if not expected_hash:
        log_error("Integrity record does not contain a hash.")
        return False

    return compare_file_hash(
        file_path,
        expected_hash,
        algorithm
    )


# ---------------------------------------------------------
# QUICK INTEGRITY CHECK
# ---------------------------------------------------------

def quick_integrity_check(file_path):
    """
    Calculate SHA-256 and display the result.
    """

    print()
    print("[*] Running quick integrity check...")

    file_hash = calculate_file_hash(
        file_path,
        "sha256"
    )

    if not file_hash:
        return False

    print()
    print("=" * 60)
    print("QUICK INTEGRITY CHECK")
    print("=" * 60)
    print(f"File   : {file_path}")
    print(f"SHA256 : {file_hash}")
    print("=" * 60)

    return True


# ---------------------------------------------------------
# INTERACTIVE MENU
# ---------------------------------------------------------

def show_menu():
    print()
    print("=" * 60)
    print("NIGHT HUNTER - FILE INTEGRITY")
    print("=" * 60)
    print("[1] Calculate File Hash")
    print("[2] Calculate Multiple Hashes")
    print("[3] Compare File Hash")
    print("[4] Compare Two Files")
    print("[5] File Information")
    print("[6] Create Integrity Record")
    print("[7] Quick SHA-256 Check")
    print("[0] Exit")
    print("=" * 60)


def interactive_mode():

    while True:

        show_menu()

        choice = input("Enter choice: ").strip()

        if choice == "0":
            print()
            print("Exiting File Integrity module...")
            break

        elif choice == "1":

            file_path = input(
                "Enter file path: "
            ).strip()

            algorithm = input(
                "Enter algorithm [sha256]: "
            ).strip()

            if not algorithm:
                algorithm = "sha256"

            file_hash = calculate_file_hash(
                file_path,
                algorithm
            )

            if file_hash:
                print()
                print("=" * 60)
                print("FILE HASH")
                print("=" * 60)
                print(f"Algorithm: {algorithm.upper()}")
                print(f"Hash     : {file_hash}")
                print("=" * 60)

        elif choice == "2":

            file_path = input(
                "Enter file path: "
            ).strip()

            display_multiple_hashes(file_path)

        elif choice == "3":

            file_path = input(
                "Enter file path: "
            ).strip()

            algorithm = input(
                "Enter algorithm [sha256]: "
            ).strip()

            if not algorithm:
                algorithm = "sha256"

            expected_hash = input(
                "Enter expected hash: "
            ).strip()

            compare_file_hash(
                file_path,
                expected_hash,
                algorithm
            )

        elif choice == "4":

            first_file = input(
                "Enter first file path: "
            ).strip()

            second_file = input(
                "Enter second file path: "
            ).strip()

            algorithm = input(
                "Enter algorithm [sha256]: "
            ).strip()

            if not algorithm:
                algorithm = "sha256"

            compare_two_files(
                first_file,
                second_file,
                algorithm
            )

        elif choice == "5":

            file_path = input(
                "Enter file path: "
            ).strip()

            display_file_information(file_path)

        elif choice == "6":

            file_path = input(
                "Enter file path: "
            ).strip()

            algorithm = input(
                "Enter algorithm [sha256]: "
            ).strip()

            if not algorithm:
                algorithm = "sha256"

            display_integrity_record(
                file_path,
                algorithm
            )

        elif choice == "7":

            file_path = input(
                "Enter file path: "
            ).strip()

            quick_integrity_check(file_path)

        else:
            print("[!] Invalid choice.")

        input("\nPress Enter to continue...")


# ---------------------------------------------------------
# DIRECT EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("NIGHT HUNTER - FILE INTEGRITY CHECKER")
    print("=" * 60)

    interactive_mode()