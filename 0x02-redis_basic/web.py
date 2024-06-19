#!/usr/bin/env python3
"""
This module provides functions for fetching HTML content from a URL,
caching it with expiration, and counting accesses using Redis.
"""
import redis
import requests


redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches HTML content from a URL, caches it with expiration,
    and counts accesses.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The HTML content of the webpage.
    """

    count_key = 'count:{}'.format(url)
    redis_client.incr(count_key)

    html_key = 'html:{}'.format(url)
    cached_html = redis_client.get(html_key)
    if cached_html:
        return cached_html.decode('utf-8')

    response = requests.get(url)
    html_content = response.text

    redis_client.setex(html_key, 10, html_content)

    return html_content
