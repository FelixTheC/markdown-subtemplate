import hashlib

import markdown2
from ..caching import cache

# Note: Do NOT enable link-patterns, it causes a crash.
__enabled_markdown_extras = [
    "cuddled-lists",
    "code-friendly",
    "fenced-code-blocks",
    "tables"
]


def transform(text, safe_mode=True):
    if not text:
        return text

    hash_val = get_hash(text)

    if entry := cache.get_html(hash_val):
        return entry.contents

    html = markdown2.markdown(text, extras=__enabled_markdown_extras, safe_mode=safe_mode)
    cache.add_html(hash_val, f"markdown_transformer:{hash_val}", '', html)

    return html


def get_hash(text):
    md5 = hashlib.md5()
    data = text.encode('utf-8')
    md5.update(data)

    return md5.hexdigest()