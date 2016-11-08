#!/usr/bin/python3
# -*- coding: utf8 -*-

from duckybot import Duckybot

if __name__ == "__main__":
    db_config = open('db_config.js', 'r')
    dict_config = json.load(db_config)
    db_config.close()

    d = Duckybot()
    d.connect_db('postgres', dict_config)
    d.install()
