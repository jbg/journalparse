from enum import Enum
import struct


class State(Enum):
    field_key = 1
    text_field_value = 2
    binary_field_size = 3
    binary_field_value = 4


def bytes_in_file(fp):
    while True:
        byte = fp.read(1)
        if byte == b'':
            break
        yield byte


def parse_entries(fp_or_iterable, entry_handler):
    state = State.field_key
    entry = {}
    buf = b""

    if hasattr(fp_or_iterable, "read"):
        fp_or_iterable = bytes_in_file(fp_or_iterable)

    for byte in fp_or_iterable:
        if state == State.field_key:
            if byte == b"=":
                key = buf
                state = State.text_field_value
                buf = b""
            elif byte == b"\n":
                if buf:
                    key = buf
                    state = State.binary_field_size
                else:
                    entry_handler(entry)
                    entry = {}
                buf = b""
            else:
                buf += byte
        elif state == State.text_field_value:
            if byte == b"\n":
                key = process_key(key.decode("utf-8"))
                buf = buf.decode("utf-8")
                entry[key] = buf
                state = State.field_key
                buf = b""
            else:
                buf += byte
        elif state == State.binary_field_size:
            if len(buf) < 8:
                buf += byte
            if len(buf) == 8:
                size = struct.unpack("<Q", buf)[0]
                state = State.binary_field_value
                buf = b""
        elif state == State.binary_field_value:
            if len(buf) < size:
                buf += byte
            elif byte == b"\n":
                key = process_key(key.decode("utf-8"))
                entry[key] = buf
                state = State.field_key
                buf = b""
            else:
                raise Exception("Expected end of data (newline) after %d bytes, got %s instead" % (size, repr(byte)))
        else:
            raise Exception("Unexpected state: %s" % state)

