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

from collections import Iterable
from .quotes_handling import *
from .core_fnc import *

__all__ = ("Varject",)


class Varject(dict):
    """
    Generate an object with all the variables stored in the specified varject file.
    Varject files are usually described using .varj, .vject or .vj
    """

    varject_list = []

    def __init__(self, filename: str):

        self._file = filename
        variables = {}

        for element in get_lines_iq(filename):
            if count_iq(element[0], ":") > 2:
                raise ConfigSyntaxError(f"To many separators line {element[1]}")
            if is_in_iq(element[0], "#"):
                element[0] = element[0][:index_iq(element[0], "#")]
            if is_in_iq(element[0], ":"):
                key = clean_string(element[0][:index_iq(element[0], ":")])
                if count_iq(element[0], ":") == 1:
                    value = clean_string(element[0][index_iq(element[0], ":") + 1:])
                else:
                    try:
                        value = transform(
                            clean_string(element[0][index_iq(element[0], ":") + 1:index_iq(element[0], ":", 2)]),
                            clean_string(element[0][index_iq(element[0], ":", 2) + 1:])
                        )
                    except TransformationError:
                        loc = {}
                        if not clean_string(element[0][index_iq(element[0], ":", 2) + 1:], False):
                            raise ConfigSyntaxError(f"Empty type value line {element[1]}")
                        try:
                            exec("var = " +
                                 repr(clean_string(element[0][index_iq(element[0], ":") + 1:index_iq(
                                     element[0], ":", 2)])) + "\nvalue = " +
                                 clean_string(element[0][index_iq(element[0], ":", 2) + 1:], False), globals(), loc)
                            value = loc["value"]
                        except Exception as error:
                            raise ConfigSyntaxError(
                                f"Invalid code or value type line {element[1]} : {error} :\n" +
                                clean_string(element[0][index_iq(element[0], ":", 2) + 1:])) from error
                if key:
                    variables[key] = value
                else:
                    raise ConfigSyntaxError(f"No key given line {element[1]}")
            elif element[0]:
                raise ConfigSyntaxError(f"No declaration line {element[1]}")
        super().__init__(variables)
        Varject.varject_list.append(self)

    def __repr__(self):
        return f"<Varject object on file {repr(self._file)} : " + \
               ", ".join(f"{repr(var)}={repr(value)}" for var, value in self.items()) + '>'

    def __str__(self):
        return super().__repr__()

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError(str(item))

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        if item in self:
            del self[item]
        raise AttributeError(str(item))

    def __dir__(self) -> Iterable[str]:
        return list(self.keys()) + list(super().__dir__())
