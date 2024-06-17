#!/usr/bin/env python3
"""
This module contains a function to retrieve schools
by topic from a MongoDB collection.

"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve schools by topic from a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The MongoDB collection to query.
        topic (str): The topic to search for.

    Returns:
        pymongo.cursor.Cursor:
            A cursor object containing the matching documents.

    """

    return mongo_collection.find({'topics': topic})
