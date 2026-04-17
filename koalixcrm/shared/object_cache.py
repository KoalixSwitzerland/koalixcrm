# -*- coding: utf-8 -*-
"""
Object cache for koalixcrm API clients.
Ported from qq_workflow_support_webapp_backend.
"""
from typing import Optional, Type, TypeVar

T = TypeVar('T')

__all__ = ['ObjectCache', 'T']


class ObjectCache:
    """Cache for storing objects to ensure each instance is only created once."""

    def __init__(self):
        self._cache = {}

    def get(self, model_class: Type[T], object_id: int) -> Optional[T]:
        """Get an object from the cache by its class and ID."""
        cache_key = (model_class.__name__, object_id)
        return self._cache.get(cache_key)

    def set(self, model_class: Type[T], object_id: int, obj: T) -> None:
        """Store an object in the cache."""
        cache_key = (model_class.__name__, object_id)
        self._cache[cache_key] = obj

    def clear(self) -> None:
        """Clear the cache."""
        self._cache = {}
