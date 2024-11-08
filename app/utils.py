import hashlib


async def transformer_function(input_str: str) -> str:
    """
    This is a transformer function that will be used to transform the input string.
    Defining this as an async function to simulate a call to an external service.
    """
    return input_str.upper()


def hash(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()


def interleave_strings(list1: list[str], list2: list[str]) -> str:
    return ", ".join(sum(zip(list1, list2), ()))
