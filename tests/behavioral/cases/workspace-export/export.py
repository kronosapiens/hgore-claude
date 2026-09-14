def export_rows(rows, workspace):
    return [row['name'] for row in rows if row['active']]
