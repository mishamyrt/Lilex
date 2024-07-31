"""Make helpers"""
import subprocess as sp
from os import listdir
from shutil import which

STAT_CONFIG = 'sources/STAT.yaml'
VARIABLE_SUFFIX = '[wght]'

def _format_variable_path(font_dir: str, family_name: str) -> str:
    return f"{font_dir}/{family_name}{VARIABLE_SUFFIX}.ttf"

def _run(*args: str) -> bool:
    with sp.Popen(" ".join(args), shell=True, stdout=sp.PIPE) as child:
        child.communicate()
        return child.returncode == 0

def _which(cmd: str) -> str:
    """shutil.which that throws on None"""
    result = which(cmd)
    if result is None:
        raise ValueError(f"""
        Can't find {cmd}. Make sure you have venv configured with
        `make configure` and activated. Alternatively, install {cmd}
        externally and check by running `which {cmd}`.
        """)
    return result

def _gftools(subcommand: str, *args: str) -> bool:
    """Runs gftools subcommand"""
    return _run(_which("gftools"), subcommand, *args)

def _fix_variable(font_dir, family_name) -> bool:
    """Generate STAT table for variable ttf"""
    file_path = _format_variable_path(font_dir, family_name)
    return _gftools(
        "fix-font",
        "--include-source-fixes",
        f'--out "{file_path}"',
        f'"{file_path}"'
    ) and _gftools(
        "gen-stat",
        "--inplace",
        f'--src "{STAT_CONFIG}"',
        f'"{file_path}"'
    )

def _fix_ttf(font_dir, _) -> bool:
    """Fix bold fsSelection and macStyle"""
    files = listdir(font_dir)
    print(files)
    for file in files:
        file_path = f'{font_dir}/{file}'
        success = _gftools(
            "fix-font",
            "--include-source-fixes",
            f'--out "{file_path}"',
            file_path
        )
        if not success:
            return False
    return True

POST_FIXES = {
    "ttf": _fix_ttf,
    "variable": _fix_variable
}

def make(family_name: str, ds_path: str, fmt: str, out_dir: str) -> bool:
    """Wrapper for fontmake"""
    cmd = [
        _which("fontmake"),
        f'-m "{ds_path}"',
        f'-o "{fmt}"',
        "--flatten-components",
        "--autohint",
        "--filter DecomposeTransformedComponentsFilter"
    ]
    if fmt == "variable":
        cmd.append(f'--output-path "{_format_variable_path(out_dir, family_name)}"')
    else:
        cmd.append("--interpolate")
        cmd.append(f'--output-dir "{out_dir}"')
    success = _run(*cmd)
    if not success:
        return False
    if fmt in POST_FIXES:
        print(f'Running fixes for {fmt}')
        success = success and POST_FIXES[fmt](out_dir, family_name)
    return success
