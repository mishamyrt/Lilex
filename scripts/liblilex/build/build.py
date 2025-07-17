"""Glyphs builder"""
import asyncio
import os
from shutil import rmtree
from tempfile import mkdtemp

from glyphsLib import GSFont, build_masters
from glyphsLib.builder.axes import find_base_style

from .constants import FontFormat
from .fontmake import fontmake
from .post_process import post_process


def _build_design_space(font: GSFont) -> str:
    """Creates temporary designspace"""
    temp_dir = mkdtemp(prefix="lilex")
    glyphs_file = os.path.join(temp_dir, "source.glyphs")
    ufo_dir = os.path.join(temp_dir, "master_ufo")
    file_name = font.familyName
    base_style = find_base_style(font.masters)
    if base_style != "":
        file_name = f"{file_name}-{base_style}"
    ds_file = os.path.join(ufo_dir, f"{file_name}.designspace")
    font.save(glyphs_file)
    build_masters(
        glyphs_file,
        ufo_dir,
        write_skipexportglyphs=True,
        designspace_path=ds_file,
    )
    return (temp_dir, ds_file)

async def _build_font(
    font: GSFont,
    output_dir: str,
    formats: list[FontFormat]
) -> list[str]:
    """Builds a font format. Returns a list of output files"""
    temp_dir, ds_file = _build_design_space(font)
    format_tasks = []
    for fmt in formats:
        out_dir = os.path.join(output_dir, fmt.value)
        format_tasks.append(fontmake(ds_file, out_dir, fmt))
    files = await asyncio.gather(*format_tasks)
    rmtree(temp_dir)
    return files

def _group_by_format(output: list[list[tuple[str, list[str]]]]) -> dict[FontFormat, list[str]]:
    result = {}
    for design_space in output:
        for fmt, files in design_space:
            if fmt not in result:
                result[fmt] = []
            result[fmt].extend(files)
    return result

async def build_family(
    fonts: list[GSFont],
    output_dir: str,
    formats: list[FontFormat]):
    """Builds a font family"""
    # Extract version from the first font
    source_font = fonts[0]
    target_version = float(f"{source_font.versionMajor}.{source_font.versionMinor}")

    tasks = []
    for font in fonts:
        tasks.append(_build_font(font, output_dir, formats))
    files = await asyncio.gather(*tasks)
    await post_process(_group_by_format(files), target_version)
    return files
