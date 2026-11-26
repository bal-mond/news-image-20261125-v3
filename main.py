#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 v3 poster.

Standard library only. Copies the pre-rendered entry.png shipped in this
repository into the directory named by MAKEFUN_OUTPUT_DIR (or /output),
then verifies the copy byte for byte: identical SHA-256 to the shipped
file, at most 1048576 bytes, valid PNG magic bytes, an IHDR chunk, and
1024x1024 dimensions. Because it only copies a fixed file, repeated runs
write identical bytes.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("main.py: error: %s" % message, file=sys.stderr)
    return 1


def read_png_size(data):
    """Return (width, height) from the IHDR chunk, or None if malformed."""
    if len(data) < 33:
        return None
    if data[0:8] != PNG_MAGIC:
        return None
    if data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest = os.path.join(out_dir, "entry.png")

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read shipped entry.png: %s" % exc)

    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the %d limit"
                    % (len(data), MAX_BYTES))

    size = read_png_size(data)
    if size is None:
        return fail("entry.png is not a valid PNG with an IHDR chunk")
    if size != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return fail("entry.png is %dx%d, expected %dx%d"
                    % (size[0], size[1], EXPECTED_WIDTH, EXPECTED_HEIGHT))

    digest = hashlib.sha256(data).hexdigest()

    if os.path.abspath(source) == os.path.abspath(dest):
        return fail("output path %s is the shipped entry.png itself" % dest)

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        return fail("cannot create output dir %s: %s" % (out_dir, exc))

    try:
        with open(dest, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        return fail("cannot write %s: %s" % (dest, exc))

    try:
        with open(dest, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        return fail("cannot re-read %s: %s" % (dest, exc))

    if hashlib.sha256(written).hexdigest() != digest:
        return fail("written copy does not match the shipped entry.png")
    if len(written) != len(data):
        return fail("written copy has the wrong length")

    print("main.py: wrote %s (%d bytes, sha256 %s)"
          % (dest, len(written), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
