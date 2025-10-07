"""Gftools wrapper"""

import asyncio
from typing import Optional

from .utils import which


async def gftools_fix(input_path: str, output_path: Optional[str] = None) -> str:
    """Wrapper for gftools.
    Args:
        input_path: The path to the font file.
        output_path: The path to the output font file.
        If not provided, the input file will be overwritten.
    Returns:
        The stdout of the gftools fix-font command.
    """
    if output_path is None:
        output_path = input_path
    cmd = [
        which("gftools"),
        "fix-font",
        "--include-source-fixes",
        f'--out "{output_path}"',
        f'"{input_path}"',
    ]
    proc = await asyncio.create_subprocess_shell(
        " ".join(cmd), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise ChildProcessError(f"gftools fix-font failed:\n{stderr.decode()}")
    return stdout.decode()
