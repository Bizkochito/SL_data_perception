def get_source_url(doc):
    url = doc["url"]
    source = url.split('/')[2].split('.')[-2]
    return source
