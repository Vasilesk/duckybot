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
        raise ValueError("dbms_name param has invalid value (see `duckybot.system.dbms.available`)")

class Dbms_base:
    """
    Base dbms class.
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
                                consumer_key text,
                                consumer_secret text,
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

    # virtual methods below

    def init_scheme(self):
        """
        Install Duckybot scheme into db.
        """
        raise NotImplementedError()

    def drop_scheme(self):
        """
        Drop Duckybot scheme in db.
        """
        raise NotImplementedError()

    def create_bot(self, codename, dict_config):
        """
        Create new bot record in db.
        """
        raise NotImplementedError()

    def update_bot(self, codename, dict_config):
        """
        Update bot record in db.
        """
        raise NotImplementedError()

    def delete_bot(self, codename):
        """
        Delete bot record from db.
        """
        raise NotImplementedError()

    def get_bot(self, codename):
        """
        Get bot record from db.
        """
        raise NotImplementedError()

    def fetch_rand_max_prior_post(self, codename):
        """
        Get random max priority post of `codename` bot decreasing the priority.
        """
        raise NotImplementedError()

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
        Postgres implementation of Dbms_base method.
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
        Postgres implementation of Dbms_base method.
        """

        cursor = self.conn.cursor()

        cursor.execute(self.drop_table_known_users)
        cursor.execute(self.drop_table_posts)
        cursor.execute(self.drop_table_bots)

        cursor.close()
        self.conn.commit()

        return True

    def create_bot(self, codename, dict_config):
        """
        Postgres implementation of Dbms_base method.
        """

        dict_config.update({'codename' : codename})
        cursor = self.conn.cursor()

        keys = dict_config.keys()
        columns = ','.join(keys)
        values = ','.join(['%({})s'.format(k) for k in keys])

        insert_query = 'INSERT INTO {0} ({1}) values ({2});'.format(self.table_bots, columns, values)
        sql_query = cursor.mogrify(insert_query, dict_config)

        cursor.execute(sql_query)
        cursor.close()
        self.conn.commit()

    def update_bot(self, codename, dict_config):
        """
        Postgres implementation of Dbms_base method.
        """

        cursor = self.conn.cursor()

        keys = dict_config.keys()
        columns = ','.join(keys)
        values = ','.join(['%({})s'.format(k) for k in keys])

        update_query = 'UPDATE {0} SET ({1})=({2}) WHERE codename=%(codename)s;'.format(self.table_bots, columns, values)

        dict_config.update({'codename' : codename})
        sql_query = cursor.mogrify(update_query, dict_config)

        cursor.execute(sql_query)
        cursor.close()
        self.conn.commit()

    def delete_bot(self, codename):
        """
        Postgres implementation of Dbms_base method.
        """

        cursor = self.conn.cursor()
        delete_query = 'DELETE FROM {0} WHERE codename = %s;'.format(self.table_bots)

        cursor.execute(delete_query, (codename, ))
        cursor.close()
        self.conn.commit()

    def get_bot(self, codename):
        """
        Postgres implementation of Dbms_base method.
        """

        cursor = self.conn.cursor()
        sql_query = """SELECT
                            sns,
                            login,
                            password,
                            consumer_key,
                            consumer_secret,
                            access_key,
                            access_secret
                        FROM """ + self.table_bots + """ WHERE codename = %s;"""
        cursor.execute(sql_query, (codename, ))
        fetched = cursor.fetchone()
        cursor.close()
        if fetched:
            return {
            'sns': fetched[0],
            'login': fetched[1],
            'password': fetched[2],
            'consumer_key': fetched[3],
            'consumer_secret': fetched[4],
            'access_key': fetched[5],
            'access_secret': fetched[6]
            }
        else:
            return False

    def fetch_rand_max_prior_post(self, codename):
        """
        Postgres implementation of Dbms_base method.
        """

        cursor = self.conn.cursor()

        sql_query = """SELECT posts.id, posts.post, max_prior, posts.bot_id
                        from ducky_posts posts
                        inner join
                        (SELECT bot_id, MAX(priority) as max_prior
                                        FROM (SELECT
                                                            ducky_posts.id,
                                                            ducky_posts.bot_id,
                                                            ducky_posts.priority
                                                        FROM
                                                            ducky_posts
                                                            INNER JOIN
                                                            ducky_bots
                                                                ON ducky_posts.bot_id=ducky_bots.id
                                                        WHERE ducky_bots.codename = %s) max_priors
                                        GROUP BY bot_id) a
                        on a.bot_id = posts.bot_id and a.max_prior = priority ORDER BY RANDOM() LIMIT 1;"""

        cursor.execute(sql_query, (codename, ))
        fetched = cursor.fetchone()

        post_id = fetched[0]
        post_text = fetched[1]

        sql_query = "UPDATE ducky_posts SET priority = priority - 1 WHERE id=%s"
        cursor.execute(sql_query, (post_id, ))

        cursor.close()
        self.conn.commit()

        return post_text
