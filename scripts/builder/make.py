"""Make helpers"""
import subprocess as sp

STAT_CONFIG = 'STAT.yaml'

def make(ds_path: str, fmt: str, out_dir: str) -> bool:
    """Wrapper for fontmake"""
    cmd = " ".join([
        "fontmake",
        f"-m '{ds_path}'",
        f"-o '{fmt}'",
        f"--output-dir '{out_dir}'",
        "--autohint",
        "--filter DecomposeTransformedComponentsFilter"
    ])
    if fmt != "variable":
        cmd += " --interpolate"
    with sp.Popen(cmd, shell=True, stdout=sp.PIPE) as child:
        child.communicate()
        return child.returncode == 0

def gen_stat(ttf_path: str):
    cmd = " ".join([
        "gftools gen-stat",
        "--inplace",
        f'--src {STAT_CONFIG}',
        ttf_path
    ])
    with sp.Popen(cmd, shell=True, stdout=sp.PIPE) as child:
        child.communicate()
        return child.returncode == 0
