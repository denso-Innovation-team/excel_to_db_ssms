from tqdm import tqdm
from typing import Optional, Iterator, Any
import time


class ProgressTracker:
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.progress_bar = tqdm(
            total=total, desc=description, unit="rows", unit_scale=True
        )
        self.start_time = time.time()

    def update(self, n: int = 1):
        """Update progress bar"""
        self.progress_bar.update(n)

    def set_postfix(self, **kwargs):
        """Set progress bar postfix"""
        self.progress_bar.set_postfix(**kwargs)

    def close(self):
        """Close progress bar and show summary"""
        elapsed_time = time.time() - self.start_time
        self.progress_bar.close()

        print(f"\n✅ Processing completed in {elapsed_time:.2f} seconds")
        print(f"📊 Average speed: {self.total/elapsed_time:.2f} rows/second")


def track_progress(
    iterator: Iterator[Any], total: int, description: str = "Processing"
):
    """Context manager for progress tracking"""
    tracker = ProgressTracker(total, description)
    try:
        for item in iterator:
            yield item
            tracker.update(len(item) if hasattr(item, "__len__") else 1)
    finally:
        tracker.close()
