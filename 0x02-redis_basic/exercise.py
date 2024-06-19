#!/usr/bin/env python3
"""
This module contains a Cache class that
interacts with Redis to store data.
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to the given method.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count calls and execute the original method.
        """

        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper


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

    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str, bytes, int, float, None
         ]:
        """
        Retrieve the value associated with the given key from Redis.

        Args:
            key (str): The key to retrieve the value for.
            fn (Optional[Callable]): An optional function to apply
                to the retrieved value.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved value,
            optionally transformed by the provided function.
        """

        data = self._redis.get(key)
        if data is None:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the value associated with the given key as a string.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Optional[str]: The value associated with the key as a string,
                or None if the key does not exist.
        """

        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the value associated with the given key from
            the Redis database and returns it as an integer.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Optional[int]: The value associated with the key as an integer,
                or None if the key does not exist.
        """

        return self.get(key, int)
