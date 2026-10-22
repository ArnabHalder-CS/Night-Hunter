# NIGHT HUNTER - Password Generator

import itertools
import secrets
import string

from core.logger import log_info, log_error


# Character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
NUMBERS = string.digits
SPECIAL = "!@#$%^&*()-_=+"


def build_charset(
    use_lowercase=True,
    use_uppercase=True,
    use_numbers=True,
    use_special=False,
    custom_characters=""
):
    """
    Build a character set based on user preferences.
    """

    characters = ""

    try:

        if use_lowercase:
            characters += LOWERCASE

        if use_uppercase:
            characters += UPPERCASE

        if use_numbers:
            characters += NUMBERS

        if use_special:
            characters += SPECIAL

        if custom_characters:
            characters += custom_characters

        # Remove duplicate characters
        characters = "".join(dict.fromkeys(characters))

        if not characters:
            raise ValueError(
                "No characters were selected."
            )

        return characters

    except Exception as error:

        log_error(
            f"Character set creation failed: {error}"
        )

        return ""


def generate_random_password(
    length=16,
    use_lowercase=True,
    use_uppercase=True,
    use_numbers=True,
    use_special=True,
    custom_characters=""
):
    """
    Generate one random password using the selected
    character types.
    """

    try:

        if length < 1:
            raise ValueError(
                "Password length must be at least 1."
            )

        characters = build_charset(
            use_lowercase,
            use_uppercase,
            use_numbers,
            use_special,
            custom_characters
        )

        if not characters:
            return ""

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        log_info(
            f"Random password generated. Length: {length}"
        )

        return password

    except Exception as error:

        log_error(
            f"Random password generation failed: {error}"
        )

        return ""


def calculate_wordlist_size(
    minimum_length,
    maximum_length,
    character_count
):
    """
    Calculate the total number of possible combinations.

    Example:

    characters = 10
    minimum = 1
    maximum = 3

    total =
    10^1 + 10^2 + 10^3
    """

    try:

        if minimum_length < 1:
            return 0

        if maximum_length < minimum_length:
            return 0

        total = 0

        for length in range(
            minimum_length,
            maximum_length + 1
        ):
            total += character_count ** length

        return total

    except Exception as error:

        log_error(
            f"Wordlist size calculation failed: {error}"
        )

        return 0


def generate_wordlist(
    minimum_length,
    maximum_length,
    output_file,
    use_lowercase=True,
    use_uppercase=True,
    use_numbers=True,
    use_special=False,
    custom_characters=""
):
    """
    Generate a Crunch-style wordlist based on
    user-selected character sets and lengths.

    The generated combinations are written directly
    to the output file instead of storing the entire
    wordlist in memory.
    """

    try:

        if minimum_length < 1:
            raise ValueError(
                "Minimum length must be at least 1."
            )

        if maximum_length < minimum_length:
            raise ValueError(
                "Maximum length cannot be smaller than minimum length."
            )

        characters = build_charset(
            use_lowercase,
            use_uppercase,
            use_numbers,
            use_special,
            custom_characters
        )

        if not characters:
            return 0

        total = calculate_wordlist_size(
            minimum_length,
            maximum_length,
            len(characters)
        )

        log_info(
            f"Character set size: {len(characters)}"
        )

        log_info(
            f"Possible combinations: {total}"
        )

        generated = 0

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            for length in range(
                minimum_length,
                maximum_length + 1
            ):

                for combination in itertools.product(
                    characters,
                    repeat=length
                ):

                    password = "".join(combination)

                    file.write(password + "\n")

                    generated += 1

        log_info(
            f"Wordlist generation completed: {generated} entries."
        )

        return generated

    except Exception as error:

        log_error(
            f"Wordlist generation failed: {error}"
        )

        return 0


def generate_pattern_wordlist(
    pattern,
    output_file,
    custom_characters=""
):
    """
    Generate combinations from a user-defined pattern.

    Supported pattern symbols:

    @ = lowercase letters
    , = uppercase letters
    % = numbers
    ^ = special characters

    Example:

    @@%%
    
    means:

    lowercase
    lowercase
    number
    number
    """

    try:

        if not pattern:
            raise ValueError(
                "Pattern cannot be empty."
            )

        character_sets = []

        for symbol in pattern:

            if symbol == "@":
                character_sets.append(LOWERCASE)

            elif symbol == ",":
                character_sets.append(UPPERCASE)

            elif symbol == "%":
                character_sets.append(NUMBERS)

            elif symbol == "^":
                character_sets.append(SPECIAL)

            elif symbol == "?":

                if custom_characters:
                    character_sets.append(
                        custom_characters
                    )
                else:
                    raise ValueError(
                        "Custom characters were not provided for '?'."
                    )

            else:
                character_sets.append(symbol)

        generated = 0

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            for combination in itertools.product(
                *character_sets
            ):

                password = "".join(combination)

                file.write(password + "\n")

                generated += 1

        log_info(
            f"Pattern wordlist generated: {generated} entries."
        )

        return generated

    except Exception as error:

        log_error(
            f"Pattern wordlist generation failed: {error}"
        )

        return 0


def generate_multiple_passwords(
    count=5,
    length=16,
    use_lowercase=True,
    use_uppercase=True,
    use_numbers=True,
    use_special=True,
    custom_characters=""
):
    """
    Generate multiple random passwords.
    """

    passwords = []

    try:

        if count < 1:
            raise ValueError(
                "Password count must be at least 1."
            )

        for _ in range(count):

            password = generate_random_password(
                length=length,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_numbers=use_numbers,
                use_special=use_special,
                custom_characters=custom_characters
            )

            if password:
                passwords.append(password)

        log_info(
            f"{len(passwords)} passwords generated."

        )

        return passwords

    except Exception as error:

        log_error(
            f"Multiple password generation failed: {error}"
        )

        return []