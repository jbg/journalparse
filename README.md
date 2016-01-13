This is a really simple Python parser for the [journald binary export format](http://www.freedesktop.org/wiki/Software/systemd/export/).

It can parse journal entries from a file-like object or an iterable, and calls a provided function for each entry with a `dict` containing all attributes of the journal entry.

    def on_journal_entry(attrs):
        print(attrs)

    with open("some_file", "rb") as fp:
        journalparse.parse_entries(fp, on_journal_entry)

    data = b"...."
    journalparse.parse_entries(data, on_journal_entry)

