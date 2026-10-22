# NIGHT HUNTER - Hash Audit Engine
#
# Password auditing for owned hashes and authorized security labs.

import hashlib
import itertools
import os
import re
import string

from core.logger import log_info, log_error


# =========================================================
# HASH DATABASE
# =========================================================

HASH_FORMATS = {
    "MD5": {
        "length": 32,
        "hashlib": "md5"
    },

    "SHA-1": {
        "length": 40,
        "hashlib": "sha1"
    },

    "SHA-224": {
        "length": 56,
        "hashlib": "sha224"
    },

    "SHA-256": {
        "length": 64,
        "hashlib": "sha256"
    },

    "SHA-384": {
        "length": 96,
        "hashlib": "sha384"
    },

    "SHA-512": {
        "length": 128,
        "hashlib": "sha512"
    },

    "SHA-512/224": {
        "length": 56,
        "hashlib": "sha512_224"
    },

    "SHA-512/256": {
        "length": 64,
        "hashlib": "sha512_256"
    },

    "SHA3-224": {
        "length": 56,
        "hashlib": "sha3_224"
    },

    "SHA3-256": {
        "length": 64,
        "hashlib": "sha3_256"
    },

    "SHA3-384": {
        "length": 96,
        "hashlib": "sha3_384"
    },

    "SHA3-512": {
        "length": 128,
        "hashlib": "sha3_512"
    },

    "BLAKE2b-512": {
        "length": 128,
        "hashlib": "blake2b"
    },

    "BLAKE2s-256": {
        "length": 64,
        "hashlib": "blake2s"
    }
}


SPECIAL_HASH_PATTERNS = {

    "bcrypt": re.compile(
        r"^\$2[aby]\$\d{2}\$"
    ),

    "Argon2": re.compile(
        r"^\$argon2(id|i|d)\$"
    ),

    "scrypt": re.compile(
        r"^\$7\$"
    ),

    "Unix crypt": re.compile(
        r"^\$[0-9A-Za-z]+\$"
    ),

    "PBKDF2": re.compile(
        r"^pbkdf2[-_]",
        re.IGNORECASE
    )
}


# =========================================================
# BASIC HASH UTILITIES
# =========================================================

def normalize_hash(hash_value):

    if not hash_value:
        return ""

    return hash_value.strip()


def is_hex_hash(hash_value):

    return bool(
        re.fullmatch(
            r"[0-9a-fA-F]+",
            hash_value
        )
    )


# =========================================================
# HASH IDENTIFICATION
# =========================================================

def identify_hash(hash_value):

    hash_value = normalize_hash(
        hash_value
    )

    result = {
        "possible_algorithms": [],
        "special_formats": [],
        "length": len(hash_value),
        "is_hex": is_hex_hash(hash_value),
        "confidence": "Unknown"
    }

    if not hash_value:
        return result


    # Check structured password-hash formats first.

    for name, pattern in SPECIAL_HASH_PATTERNS.items():

        if pattern.search(hash_value):

            result["special_formats"].append(
                name
            )


    # Check hexadecimal digest formats.

    if result["is_hex"]:

        for name, info in HASH_FORMATS.items():

            if info["length"] != len(hash_value):
                continue

            hashlib_name = info["hashlib"]

            if hashlib_name in hashlib.algorithms_available:

                result[
                    "possible_algorithms"
                ].append(name)


    if (
        result["possible_algorithms"]
        or result["special_formats"]
    ):

        result["confidence"] = (
            "Possible match - "
            "format/length based identification"
        )


    return result


# =========================================================
# HASH CALCULATION
# =========================================================

def calculate_hash(
    candidate,
    algorithm
):

    try:

        algorithm = algorithm.lower()

        if algorithm not in hashlib.algorithms_available:

            return None

        return hashlib.new(
            algorithm,
            candidate.encode("utf-8")
        ).hexdigest()


    except Exception as error:

        log_error(
            f"Hash calculation failed: {error}"
        )

        return None


# =========================================================
# VERIFY ONE CANDIDATE
# =========================================================

def verify_candidate(
    candidate,
    target_hash,
    algorithm
):

    generated = calculate_hash(
        candidate,
        algorithm
    )

    if generated is None:
        return False

    return (
        generated.lower()
        == target_hash.lower()
    )


# =========================================================
# WORDLIST ENGINE
# =========================================================

def read_wordlist(
    wordlist_path
):

    if not os.path.isfile(
        wordlist_path
    ):

        raise FileNotFoundError(
            f"Wordlist not found: {wordlist_path}"
        )


    with open(
        wordlist_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        for line in file:

            candidate = line.rstrip(
                "\r\n"
            )

            if candidate:

                yield candidate


# =========================================================
# WORDLIST STATISTICS
# =========================================================

def get_wordlist_info(
    wordlist_path
):

    total = 0
    minimum = None
    maximum = 0


    try:

        for candidate in read_wordlist(
            wordlist_path
        ):

            total += 1

            length = len(candidate)

            if minimum is None:

                minimum = length

            minimum = min(
                minimum,
                length
            )

            maximum = max(
                maximum,
                length
            )


        return {
            "path": wordlist_path,
            "entries": total,
            "minimum_length": minimum or 0,
            "maximum_length": maximum
        }


    except Exception as error:

        log_error(
            f"Unable to inspect wordlist: {error}"
        )

        return {
            "path": wordlist_path,
            "entries": 0,
            "minimum_length": 0,
            "maximum_length": 0
        }


# =========================================================
# WORDLIST AUDIT ENGINE
# =========================================================

def audit_wordlist(
    target_hash,
    algorithm,
    wordlist_path
):

    attempts = 0
    matches = []


    try:

        hashlib_name = HASH_FORMATS[
            algorithm
        ]["hashlib"]


        for candidate in read_wordlist(
            wordlist_path
        ):

            attempts += 1


            if verify_candidate(
                candidate,
                target_hash,
                hashlib_name
            ):

                matches.append(
                    candidate
                )

                log_info(
                    f"Hash match found: {candidate}"
                )

                # Exact password match found.
                # Stop because another candidate
                # is unnecessary for this hash.
                break


        return {
            "matches": matches,
            "attempts": attempts
        }


    except Exception as error:

        log_error(
            f"Wordlist audit failed: {error}"
        )

        return {
            "matches": matches,
            "attempts": attempts
        }


# =========================================================
# CHARACTER SET BUILDER
# =========================================================

def build_character_set(
    lowercase=True,
    uppercase=True,
    numbers=True,
    symbols=False,
    custom=""
):

    characters = ""


    if lowercase:

        characters += string.ascii_lowercase


    if uppercase:

        characters += string.ascii_uppercase


    if numbers:

        characters += string.digits


    if symbols:

        characters += "!@#$%^&*()-_=+"


    if custom:

        characters += custom


    # Remove duplicate characters.

    return "".join(
        dict.fromkeys(
            characters
        )
    )


# =========================================================
# SEARCH SPACE CALCULATOR
# =========================================================

def calculate_search_space(
    minimum_length,
    maximum_length,
    character_count
):

    if minimum_length < 1:
        minimum_length = 1

    if maximum_length < minimum_length:
        return 0


    total = 0


    for length in range(
        minimum_length,
        maximum_length + 1
    ):

        total += (
            character_count ** length
        )


    return total


# =========================================================
# GENERATED CANDIDATE ENGINE
# =========================================================

def generate_candidates(
    minimum_length,
    maximum_length,
    character_set
):

    if not character_set:
        return


    for length in range(
        minimum_length,
        maximum_length + 1
    ):

        for combination in itertools.product(
            character_set,
            repeat=length
        ):

            yield "".join(
                combination
            )


# =========================================================
# GENERATED AUDIT
# =========================================================

def audit_generated_candidates(
    target_hash,
    algorithm,
    minimum_length,
    maximum_length,
    character_set
):

    attempts = 0
    matches = []


    try:

        hashlib_name = HASH_FORMATS[
            algorithm
        ]["hashlib"]


        for candidate in generate_candidates(
            minimum_length,
            maximum_length,
            character_set
        ):

            attempts += 1


            if verify_candidate(
                candidate,
                target_hash,
                hashlib_name
            ):

                matches.append(
                    candidate
                )

                log_info(
                    f"Generated candidate matched: "
                    f"{candidate}"
                )

                break


        return {
            "matches": matches,
            "attempts": attempts
        }


    except Exception as error:

        log_error(
            f"Generated audit failed: {error}"
        )

        return {
            "matches": matches,
            "attempts": attempts
        }


# =========================================================
# PASSWORD VARIATION ENGINE
# =========================================================

def generate_variations(
    word
):

    variations = set()


    if not word:
        return variations


    variations.add(word)
    variations.add(word.lower())
    variations.add(word.upper())
    variations.add(word.capitalize())


    # Simple character substitutions.

    substitutions = str.maketrans({
        "a": "@",
        "A": "@",
        "i": "1",
        "I": "1",
        "o": "0",
        "O": "0",
        "s": "$",
        "S": "$",
        "e": "3",
        "E": "3"
    })


    variations.add(
        word.translate(
            substitutions
        )
    )


    # Number suffixes.

    for number in (
        "1",
        "12",
        "123",
        "1234",
        "2024",
        "2025",
        "2026"
    ):

        variations.add(
            word + number
        )


    # Symbol suffixes.

    for symbol in (
        "!",
        "@",
        "#",
        "$",
        "123!"
    ):

        variations.add(
            word + symbol
        )


    return variations


# =========================================================
# RULE-BASED WORDLIST CREATION
# =========================================================

def create_rule_candidates(
    words
):

    candidates = set()


    for word in words:

        candidates.update(
            generate_variations(
                word
            )
        )


    return candidates


# =========================================================
# PROFILE CANDIDATE ENGINE
# =========================================================

def create_profile_candidates(
    words
):

    cleaned_words = []


    for word in words:

        word = word.strip()

        if word:

            cleaned_words.append(
                word
            )


    candidates = set()


    # Individual variations.

    candidates.update(
        create_rule_candidates(
            cleaned_words
        )
    )


    # Two-word combinations.

    for first in cleaned_words:

        for second in cleaned_words:

            if first == second:
                continue


            candidates.add(
                first + second
            )

            candidates.add(
                first + second.capitalize()
            )

            candidates.add(
                first.capitalize() + second
            )

            candidates.add(
                first + "_" + second
            )

            candidates.add(
                first + "-" + second
            )


    return candidates


# =========================================================
# CANDIDATE FILE CREATOR
# =========================================================

def create_candidate_file(
    candidates,
    output_path
):

    try:

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            for candidate in sorted(
                candidates
            ):

                file.write(
                    candidate + "\n"
                )


        log_info(
            f"Candidate file created: "
            f"{output_path}"
        )


        return True


    except Exception as error:

        log_error(
            f"Unable to create candidate file: "
            f"{error}"
        )

        return False


# =========================================================
# MAIN AUDIT FUNCTION
# =========================================================

def audit_hash(
    target_hash,
    algorithm=None,
    wordlist_path=None,
    generated=False,
    minimum_length=1,
    maximum_length=4,
    character_set=""
):

    target_hash = normalize_hash(
        target_hash
    )


    identification = identify_hash(
        target_hash
    )


    possible_algorithms = identification[
        "possible_algorithms"
    ]


    if not possible_algorithms:

        return {
            "found": False,
            "matches": [],
            "attempts": 0,
            "identification": identification
        }


    # User-selected algorithm.

    if algorithm:

        selected = algorithm.strip()


        if selected not in possible_algorithms:

            return {
                "found": False,
                "matches": [],
                "attempts": 0,
                "identification": identification,
                "message":
                    "Selected algorithm is not "
                    "a possible format match."
            }


        algorithms = [
            selected
        ]

    else:

        algorithms = possible_algorithms


    all_matches = []
    total_attempts = 0


    for current_algorithm in algorithms:

        # -------------------------------------------------
        # WORDLIST
        # -------------------------------------------------

        if wordlist_path:

            result = audit_wordlist(
                target_hash,
                current_algorithm,
                wordlist_path
            )


            total_attempts += (
                result["attempts"]
            )


            for match in result["matches"]:

                all_matches.append({
                    "password": match,
                    "algorithm":
                        current_algorithm,
                    "source":
                        "wordlist"
                })


        # -------------------------------------------------
        # GENERATED CANDIDATES
        # -------------------------------------------------

        if generated:

            if not character_set:

                character_set = (
                    string.ascii_lowercase
                    + string.digits
                )


            result = audit_generated_candidates(
                target_hash,
                current_algorithm,
                minimum_length,
                maximum_length,
                character_set
            )


            total_attempts += (
                result["attempts"]
            )


            for match in result["matches"]:

                all_matches.append({
                    "password": match,
                    "algorithm":
                        current_algorithm,
                    "source":
                        "generated candidates"
                })


    return {
        "found": bool(all_matches),
        "matches": all_matches,
        "attempts": total_attempts,
        "identification": identification
    }


# =========================================================
# DISPLAY
# =========================================================

def display_audit_result(
    result
):

    print()
    print("=" * 60)
    print("                 NIGHT HUNTER")
    print("                  HASH AUDIT")
    print("=" * 60)


    identification = result.get(
        "identification",
        {}
    )


    print(
        f"Hash length: "
        f"{identification.get('length', 0)}"
    )


    print(
        f"Hexadecimal: "
        f"{identification.get('is_hex', False)}"
    )


    possible = identification.get(
        "possible_algorithms",
        []
    )


    if possible:

        print()
        print(
            "Possible algorithms:"
        )


        for algorithm in possible:

            print(
                f"  [*] {algorithm}"
            )


    special = identification.get(
        "special_formats",
        []
    )


    if special:

        print()
        print(
            "Special formats:"
        )


        for item in special:

            print(
                f"  [*] {item}"
            )


    print()
    print(
        f"Candidates tested: "
        f"{result.get('attempts', 0)}"
    )


    print("-" * 60)


    matches = result.get(
        "matches",
        []
    )


    if matches:

        print(
            "MATCH FOUND"
        )


        for match in matches:

            print()
            print(
                f"Password: "
                f"{match['password']}"
            )

            print(
                f"Algorithm: "
                f"{match['algorithm']}"
            )

            print(
                f"Source: "
                f"{match['source']}"
            )


    else:

        print(
            "NO MATCH FOUND"
        )

        print()
        print(
            "The tested candidate sources "
            "did not contain a matching password."
        )


    print("=" * 60)
    print()