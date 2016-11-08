# Copyright: 2016, Vasilii V. Bodnariuk
# Author: Vasilii V. Bodnariuk (http://vasilesk.ru)
# License: MIT
"""
The core of duckybot package: the Duckybot class.
"""

__all__ = ('Duckybot',)


from .system import sns, dbms, existent, files

class Duckybot:
    def __init__(self):
        """
        Create Duckybot instance.
        """

        self.existent = False
        self.files = files.Files

    def connect_db(self, dbms_name, dict_config):
        """
        Establish db connection.

        :param dbms_name: Database Management System name (see `system.dbms.available`)
        :param dict_config: dictionary containing data for connection
        """

        self.dbms = dbms.get_dbms_instance(dbms_name, dict_config)

    def install(self):
        """
        Install Duckybot scheme into db.
        Should be used only once.
        Requires db connection to be established (`see self.connect_db()`).
        """

        self.dbms.init_scheme()

    def uninstall(self):
        """
        Drop Duckybot scheme in db.
        Requires db connection to be established (`see self.connect_db()`).
        """

        self.dbms.drop_scheme()

    def create_new(self, codename, dict_create):
        """
        Create a new bot record in db.
        To operate this bot after creation one should call `self.operate_existent()` method.
        Requires db connection to be established (`see self.connect_db()`).

        :param codename: new bot codename
        :param dict_create: dictionary with info to create;
            possible keys:
            `sns` - new bot social networking service name (see system.sns.available)
            `login` - account login
            `password` - account password
            `access_key` - auth access key
            `access_secret` - auth access secret
        """

        self.dbms.create_bot(codename, dict_create)

    def delete_existent(self, codename):
        """
        Delete the bot from db.
        Requires db connection to be established (`see self.connect_db()`).

        :param codename: bot codename
        """

    def update_existent(self, codename, dict_update):
        """
        Update existent bot data  in db.
        Requires existent bot codename to be established (`see self.operate_existent()`).

        :param codename: bot codename
        :param dict_update: dictionary with info to update;
            possible keys:
            `sns` - new bot social networking service name (see system.sns.available)
            `login` - account login
            `password` - account password
            `access_key` - auth access key
            `access_secret` - auth access secret
        """

    def operate_existent(self, codename, auto_delay=False):
        """
        Operate bot that exists in db.
        Requires db connection to be established (`see self.connect_db()`).
        Makes `self.bot` methods available for usage.

        :param codename: existent bot codename
        :param auto_delay: if True the bot will sleep to prevent sns api limiting errors
        """

        self.bot = existent.Existent(codename=codename, auto_delay=auto_delay)
