# Copyright: 2016, Vasilii V. Bodnariuk
# Author: Vasilii V. Bodnariuk (http://vasilesk.ru)
# License: MIT
"""
Existent bot operation class
"""

class Existent:
    def __init__(self, codename, auto_delay):
        print(codename)

    def send_random_post(self):
        """
        Send a random post from db.
        Requires existent bot codename to be established (`see self.operate_existent()`).
        """

        print('random post')

    def follow_one(self, last=True, group=''):
        """
        Follow known user from db.

        :param last: if follow the last user added to db
        :param group: group of the user to follow (if specified)
        """

        print('user followed')

    def unfollow_expired_one(self, expiration_delta, last=False, group=''):
        """
        Unfollow known user from db who hasn't followed back in time.

        :param expiration_delta: time delta to consider the user expired
        :param last: if unfollow the last user expired
        :param group: group of the user to unfollow (if specified)
        """

        print('user unfollowed')
