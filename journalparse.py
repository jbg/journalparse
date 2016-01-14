import struct


class State(object):
    FieldKey, TextFieldValue, BinaryFieldSize, BinaryFieldValue = range(4)


def bytes_in_file(fp):
    while True:
        byte = fp.read(1)
        if byte == b'':
            break
        yield byte


def journalparse(fp_or_iterable, entry_handler):
    state = State.FieldKey
    entry = {}
    buf = b""

    if hasattr(fp_or_iterable, "read"):
        fp_or_iterable = bytes_in_file(fp_or_iterable)

    for byte in fp_or_iterable:
        if state == State.FieldKey:
            if byte == b"=":
                key = buf
                state = State.TextFieldValue
                buf = b""
            elif byte == b"\n":
                if buf:
                    key = buf
                    state = State.BinaryFieldSize
                else:
                    entry_handler(entry)
                    entry = {}
                buf = b""
            else:
                buf += byte
        elif state == State.TextFieldValue:
            if byte == b"\n":
                key = process_key(key.decode("utf-8"))
                buf = buf.decode("utf-8")
                entry[key] = buf
                state = State.FieldKey
                buf = b""
            else:
                buf += byte
        elif state == State.BinaryFieldSize:
            if len(buf) < 8:
                buf += byte
            if len(buf) == 8:
                size = struct.unpack("<Q", buf)[0]
                state = State.BinaryFieldValue
                buf = b""
        elif state == State.BinaryFieldValue:
            if len(buf) < size:
                buf += byte
            elif byte == b"\n":
                key = process_key(key.decode("utf-8"))
                entry[key] = buf
                state = State.FieldKey
                buf = b""
            else:
                raise Exception("Expected end of data (newline) after %d bytes, got %s instead" % (size, repr(byte)))
        else:
            raise Exception("Unexpected state: %s" % state)

