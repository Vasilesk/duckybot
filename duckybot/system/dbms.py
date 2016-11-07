# Copyright: 2016, Vasilii V. Bodnariuk
# Author: Vasilii V. Bodnariuk (http://vasilesk.ru)
# License: MIT
"""
Database Management System connection
"""

available = [
    'postgres'
]

class Postgres:
    def __init__(self):
        import psycopg2
