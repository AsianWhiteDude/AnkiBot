


def get_hint(answer: str):

    result = answer.split()[0]

    return result


def validate_set_name(text: str) -> bool:
    return 3 <= len(text) <= 30