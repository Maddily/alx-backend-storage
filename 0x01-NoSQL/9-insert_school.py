#!/usr/bin/env python3
"""
This module contains a function to insert a document
into a MongoDB collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a document into the specified MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The MongoDB collection to insert the document into.
        **kwargs: Keyword arguments representing the fields
            and values of the school document.

    Returns:
        str: The inserted document's ID.

    """

    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
