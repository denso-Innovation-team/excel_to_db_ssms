from tqdm import tqdm
from typing import Optional, Iterator, Any
import time

class ProgressTracker:
    """Progress tracker with context manager support"""
    
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
            ncols=100
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager"""
        if self.progress_bar:
            self.progress_bar.close()
        
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            print(f"\nProcessing completed in {elapsed_time:.2f} seconds")
            if self.total > 0:
                print(f"Average speed: {self.total/elapsed_time:.0f} rows/second")

    def update(self, n: int = 1):
        """Update progress bar"""
        if self.progress_bar:
            self.progress_bar.update(n)

    def set_postfix(self, **kwargs):
        """Set progress bar postfix"""
        if self.progress_bar:
            self.progress_bar.set_postfix(**kwargs)

    def close(self):
        """Manual close (for backward compatibility)"""
        if self.progress_bar:
            self.progress_bar.close()

def track_progress(iterator: Iterator[Any], total: int, description: str = "Processing"):
    """Context manager for progress tracking"""
    with ProgressTracker(total, description) as tracker:
        for item in iterator:
            yield item
            tracker.update(len(item) if hasattr(item, "__len__") else 1)
