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


async def _fix_variable(files: list[str]):
    """Generate STAT table for variable ttf"""
    fix_tasks = []
    for file in files:
        fix_tasks.append(_fix_font(file))
    await asyncio.gather(*fix_tasks)
    config = load(open(STAT_CONFIG, encoding="utf-8"), Loader=SafeLoader)
    fonts = [TTFont(f) for f in files]
    gen_stat_tables_from_config(config, fonts, has_italic=True)
    for font in fonts:
        dst = font.reader.file.name
        if os.path.isfile(dst):
            os.remove(dst)
        font.save(dst)

async def _fix_ttf(files: list[str]):
    """Fix bold fsSelection and macStyle"""
    fix_tasks = []
    for file in files:
        fix_tasks.append(_fix_font(file))
    await asyncio.gather(*fix_tasks)

POST_FIXES = {
    FontFormat.TTF: _fix_ttf,
    FontFormat.VARIABLE: _fix_variable
}

async def post_process(font_map: dict[FontFormat, list[str]]):
    """Run post fixes"""
    tasks = []
    for fmt, files in font_map.items():
        if fmt in POST_FIXES:
            tasks.append(POST_FIXES[fmt](files))
    await asyncio.gather(*tasks)
