#!/usr/bin/env python3
"""
This module contains a function to list all documents
in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    Retrieve all documents from the specified MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection to retrieve documents from.

    Returns:
        A cursor object containing all documents in the collection.
    """

    return mongo_collection.find()
