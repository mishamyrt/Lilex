"""Fonts post processing"""
import asyncio
import os

from fontTools.ttLib import TTFont
from gftools.stat import gen_stat_tables_from_config
from yaml import SafeLoader, load

from .constants import FontFormat
from .path import which

STAT_CONFIG = 'sources/STAT.yaml'

async def _gftools(subcommand: str, *args: str):
    """Wrapper for fontmake"""
    cmd = [which("gftools"), subcommand, *args]
    proc = await asyncio.create_subprocess_shell(" ".join(cmd),
                                        stdout=asyncio.subprocess.PIPE,
                                        stderr=asyncio.subprocess.PIPE)
    await proc.communicate()
    if proc.returncode != 0:
        raise ChildProcessError(f"gftools {subcommand} failed")

async def _fix_font(file: str):
    await _gftools(
        "fix-font",
        "--include-source-fixes",
        f'--out "{file}"',
        f'"{file}"'
    )

def _normalize_version(font: TTFont, target_version: float):
    """Normalize font version to fix floating point precision issues"""
    if 'head' in font:
        font['head'].fontRevision = target_version

async def _fix_variable(files: list[str], target_version: float):
    """Generate STAT table for variable ttf"""
    fix_tasks = []
    for file in files:
        fix_tasks.append(_fix_font(file))
    await asyncio.gather(*fix_tasks)
    with open(STAT_CONFIG, "r", encoding="utf-8") as file:
        config = load(file, Loader=SafeLoader)
    fonts = [TTFont(f) for f in files]
    gen_stat_tables_from_config(config, fonts, has_italic=True)
    for font in fonts:
        _normalize_version(font, target_version)
        dst = font.reader.file.name
        if os.path.isfile(dst):
            os.remove(dst)
        font.save(dst)

async def _fix_ttf(files: list[str], target_version: float):
    """Fix bold fsSelection and macStyle"""
    fix_tasks = []
    for file in files:
        fix_tasks.append(_fix_font(file))
    await asyncio.gather(*fix_tasks)
    # Normalize versions to fix floating point precision issues
    for file_path in files:
        font = TTFont(file_path)
        _normalize_version(font, target_version)
        font.save(file_path)

async def post_process(font_map: dict[FontFormat, list[str]], target_version: float):
    """Run post fixes"""
    tasks = []
    for fmt, files in font_map.items():
        if fmt == FontFormat.TTF:
            tasks.append(_fix_ttf(files, target_version))
        elif fmt == FontFormat.VARIABLE:
            tasks.append(_fix_variable(files, target_version))
    await asyncio.gather(*tasks)
