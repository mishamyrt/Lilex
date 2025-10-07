import time

ASCII_DIM = "\033[2m"
ASCII_RESET = "\033[0m"


class Stopwatch:
    """A stopwatch for measuring time"""

    def __init__(self, message: str, verbose: bool = True):
        self.message = message
        self.start_time = time.time()
        self.verbose = verbose

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.time()
        time_taken = (end_time - self.start_time) * 1000
        if self.verbose:
            print(f"{ASCII_DIM}{self.message}: {time_taken:.2f} ms{ASCII_RESET}")
