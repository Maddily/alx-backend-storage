#!/usr/bin/env python3
"""
This module contains a Cache class that
interacts with Redis to store data.
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional
import uuid


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function.
    """

    @wraps(method)
    def wrapper(self, *args):
        """
        Wrapper function to store history of inputs and outputs.
        """

        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'

        self._redis.rpush(input_key, str(args))

        output = method(self, *args)
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


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


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """

    if not callable(method):
        return

    redis_instance = getattr(method, '__self__', None)
    if not isinstance(redis_instance, Cache):
        return

    redis_client = redis_instance._redis
    method_name = method.__qualname__

    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for input_, output in zip(inputs, outputs):
        input_str = input_.decode('utf-8')
        output_str = output.decode('utf-8')
        print("{}(*{}) -> {}".format(method_name, input_str, output_str))


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
    @call_history
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
