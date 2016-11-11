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

def get_sns_instance(sns_name, dict_config, auto_delay):
    """
    Create sns instance.

    :param sns_name: name of sns (see `available`)
    :param dict_config: dictionary containing data for auth
    """

    if sns_name in available:
        return globals()[sns_name.capitalize()](dict_config, auto_delay)
    else:
        raise ValueError("bot `sns` param was not set or has invalid value (see `duckybot.system.sns.available`)")

class Sns_base:
    """
    Base sns class.
    """

    # virtual methods below

    def send_text_post(self, text):
        """
        Send post containing text only.
        """
        raise NotImplementedError()


class Twitter (Sns_base):
    def __init__(self, dict_config, auto_delay):
        import tweepy
        self.auth = tweepy.OAuthHandler(dict_config['consumer_key'], dict_config['consumer_secret'])
        self.tweepy_cursor = tweepy.Cursor
        self.auth.set_access_token(dict_config['access_key'], dict_config['access_secret'])
        self.api = tweepy.API(self.auth)

    def send_text_post(self, text):
        """
        Twitter implementation of Sns_base method.
        """

        self.api.update_status(text)
