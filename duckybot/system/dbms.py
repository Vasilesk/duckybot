# Copyright: 2016, Vasilii V. Bodnariuk
# Author: Vasilii V. Bodnariuk (http://vasilesk.ru)
# License: MIT
"""
Database Management System connection
"""

"""
Available dbms
"""
available = [
    'postgres'
]

def Dbms(dbms_name, dict_config):
    """
    Create dbms instance.

    :param dbms_name: name of dbms (see `available`)
    :param dict_config: dictionary containing data for connection
    """
    if dbms_name in available:
        return globals()[dbms_name.capitalize()](dict_config)
    else:
        raise ValueError("dbms_name param has invalid value (see `system.dbms.available`)")

class Postgres:
    def __init__(self, dict_config):
        """
        Create Postgres dbms instance.

        :param dict_config: dictionary containing data for connection
        """

        import psycopg2
        self.conn = psycopg2.connect(**dict_config)

    def init_scheme(self):
        """
        Install Duckybot scheme into db.
        """
        cursor = self.conn.cursor()
        create_table_bots = """CREATE TABLE IF NOT EXISTS bots (
                                    id serial PRIMARY KEY,
                                    codename text UNIQUE,
                                    sns text,
                                    login text,
                                    password text,
                                    access_key text,
                                    access_secret text);"""

        cursor.execute(create_table_bots)

        create_table_known_users = """CREATE TABLE IF NOT EXISTS known_users (
                                            id serial PRIMARY KEY,
                                            bot_codename text REFERENCES bots (codename) ON DELETE CASCADE,
                                            user_id text,
                                            is_follower boolean,
                                            is_friend boolean,
                                            friend_since timestamp,
                                            UNIQUE (bot_codename, user_id));"""

        cursor.execute(create_table_known_users)

        create_table_posts = """CREATE TABLE IF NOT EXISTS posts (
                                    id serial PRIMARY KEY,
                                    bot_codename text REFERENCES bots (codename) ON DELETE CASCADE,
                                    post text,
                                    priority int NOT NULL);"""

        cursor.execute(create_table_posts)

        cursor.close()
        self.conn.commit()

        return True

    def drop_scheme(self):
        """
        Drop Duckybot scheme in db.
        """
        cursor = self.conn.cursor()

        drop_table_known_users = "DROP TABLE known_users;"
        cursor.execute(drop_table_known_users)

        drop_table_posts = "DROP TABLE posts;"
        cursor.execute(drop_table_posts)

        drop_table_bots = "DROP TABLE bots;"
        cursor.execute(drop_table_bots)

        cursor.close()
        self.conn.commit()

        return True
