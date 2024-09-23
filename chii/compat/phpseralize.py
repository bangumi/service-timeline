"""
This file is copied and modified from https://github.com/mitsuhiko/phpserialize

Licensed under bsd 3-clause license
<https://github.com/mitsuhiko/phpserialize/blob/master/LICENSE>

Copyright 2021-2022 by Trim21 <trim21.me@gmail.com>
Copyright 2007-2016 by Armin Ronacher.
"""

from __future__ import annotations

from collections import OrderedDict
from io import BytesIO
from types import MappingProxyType
from typing import Any, Mapping

__all__ = (
    "dict_to_list",
    "loads",
    "dumps",
)

import six


def load(fp: BytesIO) -> Any:
    """Read a string from the open file object `fp` and interpret it as a
    data stream of PHP-serialized objects, reconstructing and returning
    the original object hierarchy.

    `fp` must provide a `read()` method that takes an integer argument.  Both
    method should return strings.  Thus `fp` can be a file object opened for
    reading, a `StringIO` object (`BytesIO` on Python 3), or any other custom
    object that meets this interface.

    `load` will read exactly one object from the stream.  See the docstring of
    the module for this chained behavior.

    If an object hook is given object-opcodes are supported in the serilization
    format.  The function is called with the class name and a dict of the
    class data members.  The data member names are in PHP format which is
    usually not what you want.  The `simple_object_hook` function can convert
    them to Python identifier names.

    If an `array_hook` is given that function is called with a list of pairs
    for all array items.  This can for example be set to
    `collections.OrderedDict` for an ordered, hashed dictionary.
    """

    def __expect(e):
        v = fp.read(len(e))
        if v != e:  # pragma: no cover
            raise ValueError(f"failed expectation, expected {e!r} got {v!r}")

    def __read_until(delim):
        buf = []
        while 1:
            char = fp.read(1)
            if char == delim:
                break
            if not char:  # pragma: no cover
                raise ValueError("unexpected end of stream")
            buf.append(char)
        return b"".join(buf)

    def __load_array():
        item_count = int(__read_until(b":"))

        __expect(b"{")

        result = []

        for _ in range(item_count):
            key = __decode()
            value = __decode()
            result.append((key, value))

        __expect(b"}")
        return result

    def __decode():
        opcode = fp.read(1)
        if opcode == b"N":
            __expect(b";")
            return None
        if opcode in b"idb":
            __expect(b":")
            data = __read_until(b";")
            if opcode == b"i":
                return int(data)
            if opcode == b"d":
                return float(data)
            return data != b"0"
        if opcode == b"s":
            __expect(b":")
            length = int(__read_until(b":"))
            __expect(b'"')
            data = fp.read(length).decode()
            __expect(b'"')
            __expect(b";")
            return data
        if opcode == b"a":
            __expect(b":")
            return dict(__load_array())
        if opcode in (b"O", b"C"):
            raise ValueError("deserialize php object is not allowed")
        raise ValueError(f"unexpected opcode {opcode}")  # pragma: no cover

    return __decode()


def loads(data: bytes | str) -> Any:
    """Read a PHP-serialized object hierarchy from a string.  Characters in the
    string past the object's representation are ignored.  On Python 3 the
    string must be a bytestring.
    """
    with BytesIO(six.ensure_binary(data)) as fp:
        return load(fp)


def dict_to_list(d: dict[int, Any]) -> list[Any]:
    """Converts an ordered dict into a list."""
    # make sure it's a dict, that way dict_to_list can be used as an
    # array_hook.
    try:
        return [d[x] for x in range(len(d))]
    except KeyError as e:  # pragma: no cover
        raise ValueError("dict is not a sequence") from e


class PHPSerializeError(Exception):
    """Bencode encode error."""


def dumps(value: Any, /) -> bytes:
    """Encode value into the phpserialize format."""
    with BytesIO() as r:
        __encode(value, r, set())
        return r.getvalue()


def __encode(value: Any, r: BytesIO, seen: set[int]) -> None:
    if isinstance(value, str):
        return __encode_bytes(value.encode("UTF-8"), r)

    if isinstance(value, int):
        return __encode_int(value, r)

    if isinstance(value, float):
        r.write(f"d:{value};".encode())
        return None

    if isinstance(value, bytes):
        return __encode_bytes(value, r)

    if isinstance(value, bool):
        if value:
            r.write(b"b:1;")
        else:
            r.write(b"b:0;")
        return None

    if value is None:
        r.write(b"N;")
        return None

    i = id(value)
    if isinstance(value, (dict, OrderedDict, MappingProxyType)):
        if i in seen:
            raise PHPSerializeError(f"circular reference found {value!r}")
        seen.add(i)
        __encode_mapping(value, r, seen)
        seen.remove(i)
        return None

    if isinstance(value, (list, tuple)):
        if i in seen:
            raise PHPSerializeError(f"circular reference found {value!r}")
        seen.add(i)

        r.write(f"a:{len(value)}:{{".encode())
        for index, item in enumerate(value):
            __encode_int(index, r)
            __encode(item, r, seen)
        r.write(b"}")

        seen.remove(i)
        return None

    if isinstance(value, bytearray):
        __encode_bytes(bytes(value), r)
        return None

    raise TypeError(f"type '{type(value)!r}' not supported")


def __encode_int(value: int, r: BytesIO) -> None:
    r.write(b"i:")
    # will handle bool and enum.IntEnum
    r.write(str(int(value)).encode())
    r.write(b";")


def __encode_bytes(x: bytes, r: BytesIO) -> None:
    r.write(b"s:")
    r.write(str(len(x)).encode())
    r.write(b':"')
    r.write(x)
    r.write(b'";')


def __encode_mapping(x: Mapping[Any, Any], r: BytesIO, seen: set[int]) -> None:
    r.write(b"a:")
    r.write(str(len(x)).encode())
    r.write(b":{")

    # force all keys to bytes, because str and bytes are incomparable
    for k, v in x.items():
        __encode_bytes(__key_to_binary(k), r)
        __encode(v, r, seen)

    r.write(b"}")


def __check_duplicated_keys(s: list[tuple[bytes, object]]) -> None:
    last_key: bytes = s[0][0]
    for current, _ in s[1:]:
        if last_key == current:
            raise PHPSerializeError(
                f"find duplicated keys {last_key!r} and {current.decode()}"
            )
        last_key = current


def __key_to_binary(key: Any) -> bytes:
    if isinstance(key, bytes):
        return key

    if isinstance(key, str):
        return key.encode()

    if isinstance(key, int):
        return str(key).encode()

    if key is None:
        return b""

    raise TypeError(f"expected value as dict key {key!r}")
