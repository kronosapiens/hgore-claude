from store import upsert


def save_tags(person_id, tags):
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise ValueError('tags must be a list of strings')
    upsert({'id': person_id, 'tags': tags})
