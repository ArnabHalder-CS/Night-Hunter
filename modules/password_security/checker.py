# NIGHT HUNTER - Password Security Checker

import re

from core.logger import log_info, log_error


# Small built-in common password list.
# User can also provide a larger custom list later.
COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "1234567890",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "welcome",
    "welcome123",
    "letmein",
    "iloveyou",
    "abc123",
    "pass123",
    "test123"
}


def check_common_password(password, password_list=None):
    """
    Check whether a password exists in the built-in
    or user-provided password list.
    """

    try:
        password_lower = password.lower()

        # Use custom list if provided
        if password_list:

            with open(
                password_list,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line in file:

                    stored_password = line.strip()

                    if stored_password.lower() == password_lower:
                        return True

            return False

        # Otherwise use built-in list
        return password_lower in COMMON_PASSWORDS

    except FileNotFoundError:

        log_error(
            f"Password list not found: {password_list}"
        )

        return False

    except Exception as error:

        log_error(
            f"Common password check failed: {error}"
        )

        return False


def check_password_patterns(password):
    """
    Check for simple password patterns.
    """

    patterns = []

    try:

        password_lower = password.lower()

        # Repeated characters
        if re.search(r"(.)\1{2,}", password):
            patterns.append(
                "Repeated characters"
            )

        # Sequential numbers
        number_sequences = [
            "123",
            "234",
            "345",
            "456",
            "567",
            "678",
            "789",
            "890"
        ]

        for sequence in number_sequences:

            if sequence in password:
                patterns.append(
                    "Sequential numbers"
                )
                break

        # Alphabet sequences
        alphabet_sequences = [
            "abc",
            "bcd",
            "cde",
            "def",
            "xyz"
        ]

        for sequence in alphabet_sequences:

            if sequence in password_lower:
                patterns.append(
                    "Sequential letters"
                )
                break

        # Keyboard patterns
        keyboard_patterns = [
            "qwerty",
            "asdf",
            "zxcv",
            "qaz",
            "wsx"
        ]

        for pattern in keyboard_patterns:

            if pattern in password_lower:
                patterns.append(
                    "Keyboard pattern"
                )
                break

        return patterns

    except Exception as error:

        log_error(
            f"Password pattern check failed: {error}"
        )

        return []


def calculate_password_score(
    password,
    password_list=None
):
    """
    Calculate a password security score.

    Maximum score = 10
    """

    score = 0
    checks = {}

    try:

        # --------------------------------
        # LENGTH
        # --------------------------------

        length = len(password)

        if length >= 16:

            score += 3
            checks["length"] = "Excellent"

        elif length >= 12:

            score += 2
            checks["length"] = "Good"

        elif length >= 8:

            score += 1
            checks["length"] = "Acceptable"

        else:

            checks["length"] = "Too Short"


        # --------------------------------
        # LOWERCASE
        # --------------------------------

        if re.search(r"[a-z]", password):

            score += 1
            checks["lowercase"] = True

        else:

            checks["lowercase"] = False


        # --------------------------------
        # UPPERCASE
        # --------------------------------

        if re.search(r"[A-Z]", password):

            score += 1
            checks["uppercase"] = True

        else:

            checks["uppercase"] = False


        # --------------------------------
        # NUMBERS
        # --------------------------------

        if re.search(r"\d", password):

            score += 1
            checks["numbers"] = True

        else:

            checks["numbers"] = False


        # --------------------------------
        # SPECIAL CHARACTERS
        # --------------------------------

        if re.search(
            r"[^A-Za-z0-9]",
            password
        ):

            score += 1
            checks["special_character"] = True

        else:

            checks["special_character"] = False


        # --------------------------------
        # COMMON PASSWORD
        # --------------------------------

        common_password = check_common_password(
            password,
            password_list
        )

        checks["common_password"] = common_password

        if common_password:

            score -= 2


        # --------------------------------
        # PATTERNS
        # --------------------------------

        patterns = check_password_patterns(
            password
        )

        checks["patterns"] = patterns

        if not patterns:

            score += 1


        # --------------------------------
        # KEEP SCORE BETWEEN 0 AND 10
        # --------------------------------

        score = max(
            0,
            min(score, 10)
        )


        # --------------------------------
        # RATING
        # --------------------------------

        if score <= 2:

            rating = "VERY WEAK"

        elif score <= 4:

            rating = "WEAK"

        elif score <= 6:

            rating = "MODERATE"

        elif score <= 8:

            rating = "STRONG"

        else:

            rating = "VERY STRONG"


        return {
            "password_length": length,
            "score": score,
            "maximum_score": 10,
            "rating": rating,
            "checks": checks
        }


    except Exception as error:

        log_error(
            f"Password score calculation failed: {error}"
        )

        return {
            "password_length": len(password),
            "score": 0,
            "maximum_score": 10,
            "rating": "UNKNOWN",
            "checks": {}
        }


def get_password_suggestions(result):
    """
    Generate suggestions based on the password analysis.
    """

    suggestions = []

    try:

        checks = result["checks"]

        if result["password_length"] < 8:

            suggestions.append(
                "Use at least 8 characters."
            )

        elif result["password_length"] < 12:

            suggestions.append(
                "Use a longer password, preferably 12+ characters."
            )

        if not checks.get("lowercase"):

            suggestions.append(
                "Add lowercase letters."
            )

        if not checks.get("uppercase"):

            suggestions.append(
                "Add uppercase letters."
            )

        if not checks.get("numbers"):

            suggestions.append(
                "Add numbers."
            )

        if not checks.get("special_character"):

            suggestions.append(
                "Add special characters."
            )

        if checks.get("common_password"):

            suggestions.append(
                "Avoid commonly used passwords."
            )

        if checks.get("patterns"):

            suggestions.append(
                "Avoid predictable or repeated patterns."
            )

        if not suggestions:

            suggestions.append(
                "Password has good security characteristics."
            )

        return suggestions

    except Exception as error:

        log_error(
            f"Password suggestion generation failed: {error}"
        )

        return []


def analyze_password(
    password,
    password_list=None
):
    """
    Complete password security analysis.
    """

    try:

        log_info(
            "Starting password security analysis."
        )

        result = calculate_password_score(
            password,
            password_list
        )

        result["suggestions"] = (
            get_password_suggestions(result)
        )

        log_info(
            f"Password rating: {result['rating']}"
        )

        return result

    except Exception as error:

        log_error(
            f"Password analysis failed: {error}"
        )

        return {}


def display_password_analysis(result):
    """
    Display password analysis in terminal.
    """

    try:

        print()
        print("================================")
        print("       PASSWORD ANALYSIS")
        print("================================")

        print(
            f"Password Length      : "
            f"{result.get('password_length', 0)}"
        )

        checks = result.get(
            "checks",
            {}
        )

        print(
            f"Lowercase Letters   : "
            f"{'YES' if checks.get('lowercase') else 'NO'}"
        )

        print(
            f"Uppercase Letters   : "
            f"{'YES' if checks.get('uppercase') else 'NO'}"
        )

        print(
            f"Numbers             : "
            f"{'YES' if checks.get('numbers') else 'NO'}"
        )

        print(
            f"Special Characters  : "
            f"{'YES' if checks.get('special_character') else 'NO'}"
        )

        print(
            f"Common Password     : "
            f"{'YES' if checks.get('common_password') else 'NO'}"
        )

        patterns = checks.get(
            "patterns",
            []
        )

        if patterns:

            print(
                "Patterns            : "
                + ", ".join(patterns)
            )

        else:

            print(
                "Patterns            : None detected"
            )

        print("--------------------------------")

        print(
            f"Security Score      : "
            f"{result.get('score', 0)}/"
            f"{result.get('maximum_score', 10)}"
        )

        print(
            f"Password Rating     : "
            f"{result.get('rating', 'UNKNOWN')}"
        )

        print("--------------------------------")

        print("Suggestions:")

        for suggestion in result.get(
            "suggestions",
            []
        ):

            print(
                f"- {suggestion}"
            )

        print("================================")
        print()

    except Exception as error:

        log_error(
            f"Unable to display password analysis: {error}"
        )