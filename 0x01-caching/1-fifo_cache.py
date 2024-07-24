#!/usr/bin/env python3
"""this is the caching module.
"""
from collections import OrderedDict

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """shows object that allows storing and
    getting items from a dictionary with a FIFO
    that has mechanism for removal when the limit is reached.
    """
    def __init__(self):
        """this creates the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """this adds an item in the cache.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", first_key)

    def get(self, key):
        """this gets an item by key.
        """
        return self.cache_data.get(key, None)
