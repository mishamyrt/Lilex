"""Generate .env file for the preview site."""

import re

from arrrgs import arg, command, run
from fontTools.ttLib import TTFont


def find_version_in_name_table(font):
    version_string = ""
    for record in font["name"].names:
        if record.nameID == 5:
            try:
                if record.platformID == 3 and record.platEncID in (1, 10):
                    version_string = record.string.decode("utf-16-be")
                    break
                version_string = record.string.decode("latin-1")
            except UnicodeDecodeError:
                version_string = record.string.decode("utf-8", "ignore")

    if version_string:
        match = re.search(r"(\d+\.\d+)", version_string)
        if match:
            return match.group(1)
    return None


@command(
    arg("font_path", help="Path to the Lilex-Regular.ttf font file."),
    arg("output_path", help="Path to the output .env file for Astro."),
    root=True,
)
def generate(args):
    """Generate .env file for the preview site."""

    font = TTFont(args.font_path)
    version = find_version_in_name_table(font)

    if not version:
        version_number = font["head"].fontRevision
        version = f"{version_number:.3f}".rstrip("0").rstrip(".")

    glyphs_count = len(font.getGlyphOrder())

    with open(args.output_path, "w", encoding="utf-8") as f:
        f.write(f"PUBLIC_LILEX_VERSION={version}\n")
        f.write(f"PUBLIC_LILEX_GLYPHS_COUNT={glyphs_count}\n")

    print(f"Generated environment for Astro at {args.output_path}")


if __name__ == "__main__":
    run()
