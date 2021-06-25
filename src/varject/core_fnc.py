"""
The MIT License (MIT)
Copyright (c) 2021 Kyrela
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


__all__ = ("clean_string", "transform", "TransformationError",)


def is_only_preceded_by(string: str, to_find: str, preceded: str) -> bool:
    """
    check if an element in a string is only preceded
    by the indicated character, even multiple times.
    Raise an ValueError if to_find is not found

    :param string: the string to search in
    :param to_find: the string to search for
    :param preceded: the string 'to_find' is supposed to be preceded
    :return: True or False
    """

    index = 0
    while index != string.index(to_find):
        if preceded != string[index:index + len(preceded)]:
            return False
        index += len(preceded)
    return True


def reformat(string: str) -> str:
    """
    format special characters such as \n, \\ and more.

    :param string: the string to format
    :return: the formatted string
    """

    import re
    import codecs

    escape_sequence_re = re.compile(r'''
        ( \\U........      # 8-digit hex escapes
        | \\u....          # 4-digit hex escapes
        | \\x..            # 2-digit hex escapes
        | \\[0-7]{1,3}     # Octal escapes
        | \\N{[^}]+}       # Unicode characters by name
        | \\[\\'"abfnrtv]  # Single-character escapes
        )''', re.UNICODE | re.VERBOSE)

    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return escape_sequence_re.sub(decode_match, string)


def clean_string(string: str, should_hard_format=True) -> str:
    """
    returns the string but formated proprely.

    :param string: the string to format
    :param should_hard_format: precise if it should check the
    presence of quotes and backslashes instead of just spaces and hasthags
    :return: the formated string
    """

    if "#" in string:
        string = string[:string.index("#")]
    while string and string[0] == " ":
        string = string[1:]
    while string and string[-1] == " ":
        string = string[:-1]
    if should_hard_format and len(string) >= 2 and string[0] == "\"" == string[-1]:
        string = string[1:-1]
        string = reformat(string)
    return string


def base_int(string: str) -> int:
    """
    convert a str to int by detecting automaticaly
    the type of the int

    :param string: the string to convert
    :return: the int
    """

    if len(string) > 1 and string[0:2] == ("0x" or "0X"):
        return int(string[2:], 16)
    if len(string) > 0 and string[0] == "0":
        return int(string[1:], 8)
    if len(string) > 1 and string[0:2] == ("0b" or "0B"):
        return int(string[2:], 16)
    return int(string)


class TransformationError(Exception):
    pass


def transform(element: str, mode: str):
    """
    transforms a string by applying to it the indicated function

    :param element: the character string to be transformed
    :param mode: the function to apply to it (int(), eval(), etc)
    :return: the transformed variable
    """

    if mode == "str" or mode == "str()":
        return str(element)
    elif mode == "bool" or mode == "bool()":
        return bool(element)
    elif mode == "int" or mode == "int()":
        return base_int(element)
    elif mode == "eval" or mode == "eval()":
        return eval(element)
    elif mode == "list" or mode == "list()":
        return list(element)
    elif mode == "float" or mode == "float()":
        return eval(element)
    elif mode == "len" or mode == "len()":
        return len(element)
    elif mode == "enumrate" or mode == "enumerate()":
        return enumerate(element)
    elif mode == "max" or mode == "max()":
        return max(element)
    elif mode == "min" or mode == "min()":
        return min(element)
    elif mode == "sorted" or mode == "sorted()":
        return sorted(element)
    elif mode == "choice" or mode == "choice()":
        import random
        return random.choice(element)
    elif mode == "date" or mode == "date()":
        from datetime import date
        return date.fromisoformat(element)
    elif mode == "time" or mode == "time()":
        from datetime import time
        return time.fromisoformat(element)
    elif mode == "datetime" or mode == "datetime()":
        from datetime import datetime
        return datetime.fromisoformat(element)
    else:
        raise TransformationError(f"Incorrect tranformation mode ({mode})")
