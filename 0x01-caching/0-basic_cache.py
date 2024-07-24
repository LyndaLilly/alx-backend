#!/usr/bin/env python3

'''This the dictionary
'''


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    '''This is a class BasicCache that inherits
       and is a caching system
    '''

    def put(self, key, item):
        '''this assign to the dictionary self.cache_data
           and the item value for the key
        '''
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        '''this returns the value in self.cache_data attached to key
        '''

        return self.cache_data.get(key, None)
