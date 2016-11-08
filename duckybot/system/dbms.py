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

def get_dbms_instance(dbms_name, dict_config):
    """
    Create dbms instance.

    :param dbms_name: name of dbms (see `available`)
    :param dict_config: dictionary containing data for connection
    """

    if dbms_name in available:
        return globals()[dbms_name.capitalize()](dict_config)
    else:
        raise ValueError("dbms_name param has invalid value (see `system.dbms.available`)")

class Dbms_base:
    """
    Base dbms class
    """

    table_bots = 'ducky_bots'
    table_known_users = 'ducky_known_users'
    table_posts = 'ducky_posts'

    create_table_bots = """CREATE TABLE IF NOT EXISTS """ + table_bots + """ (
                                id serial PRIMARY KEY,
                                codename text UNIQUE,
                                sns text,
                                login text,
                                password text,
                                access_key text,
                                access_secret text);"""

    drop_table_bots = "DROP TABLE " + table_bots + ";"

    create_table_known_users = """CREATE TABLE IF NOT EXISTS """ + table_known_users + """ (
                                        id serial PRIMARY KEY,
                                        bot_id integer REFERENCES """ + table_bots + """ (id) ON DELETE CASCADE,
                                        user_id text,
                                        is_follower boolean,
                                        is_friend boolean,
                                        friend_since timestamp,
                                        UNIQUE (bot_id, user_id));"""

    drop_table_known_users = "DROP TABLE " + table_known_users + ";"

    create_table_posts = """CREATE TABLE IF NOT EXISTS """ + table_posts + """ (
                                id serial PRIMARY KEY,
                                bot_id integer REFERENCES """ + table_bots + """ (id) ON DELETE CASCADE,
                                post text,
                                priority int NOT NULL);"""

    drop_table_posts = "DROP TABLE " + table_posts + ";"

    def get_insert_query(self, table_name, dict_data):
        l = [(c, v) for c, v in dict_data.items()]
        columns = ','.join([t[0] for t in l])
        values = tuple([t[1] for t in l])

        return 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table_name, columns, values)

class Postgres (Dbms_base):
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

        cursor.execute(self.create_table_bots)
        cursor.execute(self.create_table_known_users)
        cursor.execute(self.create_table_posts)

        cursor.close()
        self.conn.commit()

        return True

    def drop_scheme(self):
        """
        Drop Duckybot scheme in db.
        """

        cursor = self.conn.cursor()

        cursor.execute(self.drop_table_known_users)
        cursor.execute(self.drop_table_posts)
        cursor.execute(self.drop_table_bots)

        cursor.close()
        self.conn.commit()

        return True

    def create_bot(self, codename, dict_create):
        """
        Create new bot record in db.
        TODO: delete id return
        """

        cursor = self.conn.cursor()
        sql_query = self.get_insert_query(self.table_bots, dict_config)
        cursor.execute(sql_query)
        cursor.close()
        self.conn.commit()
