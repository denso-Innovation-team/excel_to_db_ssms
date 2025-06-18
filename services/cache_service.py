from typing import Any, Dict
import pickle
from pathlib import Path
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Enhanced caching service"""

    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = 3600  # 1 hour

    def get(self, key: str, default: Any = None) -> Any:
        """Get cached value"""
        # Try memory cache first
        if key in self.memory_cache:
            cache_data = self.memory_cache[key]
            if not self._is_expired(cache_data["timestamp"], cache_data["ttl"]):
                return cache_data["value"]
            else:
                del self.memory_cache[key]

        # Try file cache
        cache_file = self.cache_dir / f"{key}.cache"
        if cache_file.exists():
            try:
                with open(cache_file, "rb") as f:
                    cache_data = pickle.load(f)
                    if not self._is_expired(cache_data["timestamp"], cache_data["ttl"]):
                        # Update memory cache
                        self.memory_cache[key] = cache_data
                        return cache_data["value"]
                    else:
                        cache_file.unlink()
            except Exception as e:
                logger.error(f"Cache read error: {e}")

        return default

    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set cache value"""
        try:
            cache_data = {
                "value": value,
                "timestamp": datetime.now(),
                "ttl": ttl or self.default_ttl,
            }

            # Update memory cache
            self.memory_cache[key] = cache_data

            # Update file cache
            cache_file = self.cache_dir / f"{key}.cache"
            with open(cache_file, "wb") as f:
                pickle.dump(cache_data, f)

            return True

        except Exception as e:
            logger.error(f"Cache write error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete cached value"""
        try:
            # Remove from memory cache
            if key in self.memory_cache:
                del self.memory_cache[key]

            # Remove file cache
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                cache_file.unlink()

            return True

        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def clear(self) -> bool:
        """Clear all cache"""
        try:
            # Clear memory cache
            self.memory_cache.clear()

            # Clear file cache
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()

            return True

        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False

    def _is_expired(self, timestamp: datetime, ttl: int) -> bool:
        """Check if cache is expired"""
        return datetime.now() > timestamp + timedelta(seconds=ttl)
