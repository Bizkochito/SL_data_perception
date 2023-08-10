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
    for source in fr_sources:
        if source in doc["url"]:
            return 'fr'
    for source in nl_sources:
        if source in doc["url"]:
            return 'nl'  
    return None
