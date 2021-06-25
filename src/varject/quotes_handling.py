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


__all__ = ("get_lines_iq", "count_iq", "ConfigSyntaxError", "is_in_iq", "index_iq",)


class ConfigSyntaxError(Exception):
    pass


def is_quote(string: str, quote_index: int, is_looking_for_opening: bool) -> bool:
    """
    indicates whether the quote str[quote_index] is an opening/closing quote

    :param string: the character string where the quote is located
    :param quote_index: the index of the quote in string
    :param is_looking_for_opening: True if you are looking for an opening quote, False for a closing quote
    :return: True if it is a delimiting quote corresponding to the corresponding to the type requested, False otherwise
    """

    if is_looking_for_opening:
        j = quote_index - 1
        if j < 0:
            j = 0
        while j > 0 and string[j] == ' ':
            j -= 1
        if j == 0 or string[j] == ":":
            return True
        else:
            return False
    else:
        j = quote_index + 1
        if j > len(string) - 1:
            j = len(string) - 1
        while j < len(string) - 1 and string[j] == ' ':
            j += 1
        temp = quote_index - 1
        if temp < 0:
            temp = 0
        if (j == len(string) - 1 or string[j] == ":") and string[temp] != "\\":
            return True
        else:
            return False


def get_lines_iq(filename: str) -> list:
    """
    separates the string on line breaks, unless the line break is between double quotes

    :param filename: the file whose lines we want to retrieve
    :return: a list containing each line as a list, with the content in [0] and the line number in [1]
    """

    lignes = []
    with open(filename, "r", encoding="utf-8") as file:
        file_ctn = file.read()
    file_ctn = file_ctn.split("\n")
    is_prec_open = False
    is_open = False
    for nb, line in enumerate(file_ctn):
        for i, char in enumerate(line):
            if char == "\"" and not is_open and is_quote(line, i, True):
                is_open = True
            elif char == "\"" and is_open and is_quote(line, i, False):
                is_open = False
        if is_prec_open:
            lignes[len(lignes) - 1][0] += line
        else:
            lignes.append([line, nb + 1])
        is_prec_open = is_open
    if is_open:
        raise ConfigSyntaxError(f"Quote never closed")
    return lignes


def is_in_iq(string: str, to_search: str, is_open=False) -> bool:
    """
    search if a char is in the indicated string

    :param string: the string to search in
    :param to_search: the char to be searched for
    :param is_open: indicates whether the string is already open
    :return: True if the element is in the string, False otherwise
    """

    for i, char in enumerate(string):
        if not is_open:
            if char == "\"" and not is_open and is_quote(string, i, True):
                is_open = True
            if char == to_search:
                return True
        if char == "\"" and is_open and is_quote(string, i, False):
            is_open = False
    return False


def count_iq(string: str, to_count: str, is_open=False) -> int:
    """
    counts the number of times a char is present but avoids those present in a quoted text

    :param string: the chain to count in
    :param to_count: the char to be counted
    :param is_open: indicates whether the string is already open
    :return: the number of times to_count is present
    """

    counted = 0
    for i, char in enumerate(string):
        if not is_open:
            if char == "\"" and not is_open and is_quote(string, i, True):
                is_open = True
            if char == to_count:
                counted += 1
        if char == "\"" and is_open and is_quote(string, i, False):
            is_open = False
    return counted


def index_iq(string: str, to_index: str, number=1, is_open=False) -> int:
    """
    gives the index of a char avoiding elements in a quoted text

    :param string: the string to search in
    :param to_index: the char to be researched
    :param number: The nth item to search for
    :param is_open: indicates whether the string is already open
    :return: the index of the element
    """

    counted = 0
    for i, char in enumerate(string):
        if not is_open:
            if char == "\"" and not is_open and is_quote(string, i, True):
                is_open = True
            if char == to_index:
                counted += 1
            if counted == number:
                return i
        if char == "\"" and is_open and is_quote(string, i, False):
            is_open = False
    raise ValueError("substring not found")
