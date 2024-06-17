#!/usr/bin/env python3
"""
This module contains a function for calculating
the average score of students in a MongoDB collection.
"""


def top_students(mongo_collection):
    """
    Calculate the average score of students in a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The MongoDB collection containing student documents.

    Returns:
        pymongo.cursor.Cursor: A cursor object containing
            the student documents sorted by average score in descending order.
    """

    sum = 0
    count = 0

    documents = mongo_collection.find()
    for document in documents:
        for topic in document['topics']:
            count += 1
            sum += topic['score']
        if count:
            average_score = sum / count
            mongo_collection.update_one({'name': document['name']},
                                        {'$set': {
                                            'averageScore': average_score
                                        }})
        sum = 0
        count = 0

    return mongo_collection.find().sort('averageScore', -1)
