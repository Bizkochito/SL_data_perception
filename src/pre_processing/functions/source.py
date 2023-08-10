def get_source_url(doc):
    url = doc["url"]
    source = url.split(".")[1]
    if "source" in doc:
        return None
    else:
        return source
