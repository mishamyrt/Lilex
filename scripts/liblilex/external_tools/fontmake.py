"""Fontmake wrapper"""

import asyncio
import os
import re
from enum import StrEnum

from .utils import which

ERROR_RE = re.compile(r"^(?:ERROR:|.*\bError:).*$", re.MULTILINE)


class FontFormat(StrEnum):
    """Font formats supported by fontmake"""

    TTF = "ttf"
    OTF = "otf"
    VARIABLE = "variable"


async def fontmake(
    design_space_path: str, out_dir: str, fmt: FontFormat, axis: list[str] = None
) -> list[str]:
    """Wrapper for fontmake.
    Args:
        design_space_path: The path to the design space file.
        out_dir: The directory to write the output files to.
        fmt: The format of the output files.
        axis: The axis values to use for the variable font.
    Returns:
        A list of the output files.
    """
    if axis is None:
        axis = ["wght"]
    cmd = [
        which("fontmake"),
        f'-m "{design_space_path}"',
        f'-o "{fmt.value}"',
        "--flatten-components",
        "--autohint",
        "--filter DecomposeTransformedComponentsFilter",
    ]
    font_name = os.path.basename(design_space_path).split(".")[0]
    if fmt == FontFormat.VARIABLE:
        cmd.append(f'--output-path "{_format_variable_path(out_dir, font_name, axis)}"')
    else:
        cmd.append("--interpolate")
        cmd.append(f'--output-dir "{out_dir}"')
    proc = await asyncio.create_subprocess_shell(
        " ".join(cmd), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await proc.communicate()
    log_text = stderr.decode()
    errors = _extract_errors(log_text)
    if errors:
        raise ChildProcessError(f"Fontmake failed: {errors}")
    files = _extract_files(log_text, out_dir)
    if not files:
        raise RuntimeError("Fontmake failed: no files found")
    return files


def _extract_errors(log_text: str) -> list[str]:
    """Extracts error lines from log text."""
    return ERROR_RE.findall(log_text)


def _extract_files(log_text: str, out_dir: str) -> list[str]:
    """Extracts file lines from log text."""
    file_re = re.escape(out_dir) + r"/(.*)"
    matches = re.findall(file_re, log_text, flags=re.MULTILINE)
    files = map(lambda x: os.path.join(out_dir, x), matches)
    return list(set(files))


def _format_variable_path(font_dir: str, family_name: str, axis: list[str]) -> str:
    """Formats the variable font file path according to Google Fonts convention"""
    file_name = f"{family_name}[{','.join(axis)}].ttf"
    return os.path.join(font_dir, file_name)
