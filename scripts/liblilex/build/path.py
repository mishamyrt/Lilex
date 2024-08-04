"""Path helpers"""
import shutil


def which(cmd: str) -> str:
    """shutil.which that throws on None"""
    result = shutil.which(cmd)
    if result is None:
        raise ValueError(f"""
        Can't find {cmd}. Make sure you have venv configured with
        `make configure` and activated. Alternatively, install {cmd}
        externally and check by running `which {cmd}`.
        """)
    return result
