"""Lilex builder constants"""

SUPPORTED_FORMATS = [
    "ttf",
    "otf",
    "variable"
]

DEFAULT_FORMATS = [
    "ttf",
    "variable"
]

NAME_TPL = {
    "ss": (
        "featureNames {\n"
        "  name 3 1 0x0409 \"$NAME\";\n"
        "};\n"
    ),
    "cv": (
        "cvParameters {\n"
        "  FeatUILabelNameID{\n"
        "    name 3 1 0x0409 \"$NAME\";\n"
        "  };\n"
        "};\n"
    )
}
