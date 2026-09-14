_rows = {}


def upsert(row):
    _rows[row['id']] = row


def load_all():
    return list(_rows.values())
