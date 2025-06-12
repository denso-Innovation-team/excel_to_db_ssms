from tqdm import tqdm
import time


class ProgressTracker:
    """Fixed Progress tracker with context manager support"""

    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.description = description
        self.progress_bar = None
        self.start_time = None

    def __enter__(self):
        """Enter context manager"""
        self.start_time = time.time()
        self.progress_bar = tqdm(
            total=self.total,
            desc=self.description,
            unit="rows",
            unit_scale=True,
            ncols=100,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager"""
        if self.progress_bar:
            self.progress_bar.close()

    def update(self, n: int = 1):
        """Update progress bar"""
        if self.progress_bar:
            self.progress_bar.update(n)

    def set_postfix(self, postfix_dict):
        """Set progress bar postfix - Fixed signature"""
        if self.progress_bar:
            self.progress_bar.set_postfix(postfix_dict)

    def close(self):
        """Manual close"""
        if self.progress_bar:
            self.progress_bar.close()
