#!/usr/bin/python3
# -*- coding: utf8 -*-

from duckybot import Duckybot

if __name__ == "__main__":
    d = Duckybot()
    d.operate_existent('a')
    d.bot.send_random_post()
    d.bot.follow_one()
