#!/usr/bin/env python3
"""
This module contains a Cache class that
interacts with Redis to store data.
"""
import redis
from typing import Union, Callable, Optional
import uuid


class Cache:
    """
    Cache class for storing data in Redis.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the Cache class.
        """

        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis and returns the generated key.

        Args:
            data: The data to be stored.
                It can be a string, bytes, int, or float.

        Returns:
            The generated key used to store the data in Redis.
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
