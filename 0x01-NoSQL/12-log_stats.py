#!/usr/bin/env python3
"""
This script retrieves and displays statistics
from a MongoDB collection of nginx logs.
"""

if __name__ == '__main__':
    import pymongo

    client = pymongo.MongoClient()
    nginx_collection = client.logs.nginx

    print(nginx_collection.count_documents({}), 'logs')
    print('Methods:')

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        print(f'\tmethod {method}:',
              nginx_collection.count_documents({'method': method}))

    print(nginx_collection.count_documents({
        'method': 'GET',
        'path': '/status'
    }), 'status check')
