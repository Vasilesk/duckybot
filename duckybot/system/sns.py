# Copyright: 2016, Vasilii V. Bodnariuk
# Author: Vasilii V. Bodnariuk (http://vasilesk.ru)
# License: MIT
"""
Social networking service api
"""

available = [
    'twitter',
    'vk'
]

class Twitter:
    def __init__(self):
        import tweepy
        print('Twi')
