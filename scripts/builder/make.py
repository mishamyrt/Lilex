"""Make helpers"""
import subprocess as sp


def make(ds_path: str, fmt: str, out_dir: str) -> bool:
    """Wrapper for fontmake"""
    cmd = " ".join([
        "fontmake",
        f"-m '{ds_path}'",
        f"-o '{fmt}'",
        f"--output-dir '{out_dir}'",
        "--autohint"
    ])
    if fmt != "variable":
        cmd += " --interpolate"
    with sp.Popen(cmd, shell=True, stdout=sp.PIPE) as child:
        child.communicate()
        return child.returncode == 0
