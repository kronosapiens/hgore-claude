from store import load_all


def segment_members(segment):
    return [row['id'] for row in load_all() if segment in row['tags'].split(',')]
