"""Stable STBL identifiers and native, reorderable localization tokens."""

import zlib

from sims4.localization import _create_localized_string


def string_key(name):
    return zlib.crc32(("valeries_jobs." + name).encode("utf-8")) & 0xffffffff


def text(name, *tokens):
    return _create_localized_string(string_key(name), *tokens)
