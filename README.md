This is a really simple Python parser for the [journald binary export format](http://www.freedesktop.org/wiki/Software/systemd/export/).

It can parse journal entries from a file-like object or an iterable, and calls a provided function for each entry with a `dict` containing all attributes of the journal entry.

    from journalparse import journalparse


    with open("some_file", "rb") as fp:
        journalparse(fp, lambda entry: print(entry))

    # ... or ...

    data = b"_MESSAGE=blah"
    journalparse(data, lambda entry: print(entry))

No requirements other than Python. Tested on Python 3.5 but should work on Python 2.6+ and 3.2+.
