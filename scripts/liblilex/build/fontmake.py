"""Make helpers"""
import asyncio
import os
import re

from .constants import FontFormat
from .path import which


def _format_variable_path(font_dir: str, family_name: str, axis: list[str]) -> str:
    return f"{font_dir}/{family_name}[{','.join(axis)}].ttf"

async def fontmake(
    design_space_path: str,
    out_dir: str,
    fmt: FontFormat,
    axis: list[str] = None
):
    """Wrapper for fontmake"""
    if axis is None:
        axis = ["wght"]
    cmd = [
        which("fontmake"),
        f'-m "{design_space_path}"',
        f'-o "{fmt.value}"',
        "--flatten-components",
        "--autohint",
        "--filter DecomposeTransformedComponentsFilter"
    ]
    font_name = os.path.basename(design_space_path).split(".")[0]
    if fmt == FontFormat.VARIABLE:
        cmd.append(f'--output-path "{_format_variable_path(out_dir, font_name, axis)}"')
    else:
        cmd.append("--interpolate")
        cmd.append(f'--output-dir "{out_dir}"')
    proc = await asyncio.create_subprocess_shell(" ".join(cmd),
                                        stdout=asyncio.subprocess.PIPE,
                                        stderr=asyncio.subprocess.PIPE)
    _, stderr = await proc.communicate()
    file_re = re.escape(out_dir) + r"/(.*)"
    matches = re.findall(file_re, stderr.decode(), flags=re.MULTILINE)
    files = []
    for match in matches:
        files.append(os.path.join(out_dir, match))
    return fmt, list(set(files))
