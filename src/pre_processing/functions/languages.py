fr_sources = [
    "rtbf",
    "lesoir",
    "dhnet",
    "lalibre",
    "sudinfo",
    "levif",
    "lavenir",
    "lecho",
]
nl_sources = ["tijd", "demorgen", "vrt", "hln", "knack"]


def language_getter(doc):
    if "source" not in doc:
        return None
    source = doc["source"]
    if source in fr_sources:
        return "fr"
    elif source in nl_sources:
        return "nl"
    else:
        return None
