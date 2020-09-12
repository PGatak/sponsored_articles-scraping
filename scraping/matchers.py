import re

TAG_PATTERNS = {
    "SPONSORED": [
        "(artyk|publik).* spons.*"
    ],
    "sponsorowan": [
        "sponsorowan.*"
    ],
    "reklamowy.*": [
        "reklamowy.*"
    ],
    "partnerski": [
        "artykuł partnerski.*"
    ]
}

# compile all regexes (optimisation):
for tag, regexes in TAG_PATTERNS.items():
    TAG_PATTERNS[tag] = [re.compile(r, re.I) for r in regexes
                         ]
    print(TAG_PATTERNS)


def match_tags(text):
    matched_tags = set()
    for tag, regexes in TAG_PATTERNS.items():
        for r in regexes:
            if r.findall(text):
                matched_tags.add(tag)
    return matched_tags
