__title__ = 'starbase.client.connection'
__author__ = 'Artur Barseghyan'
__all__ = ('Connection',)

from starbase.exceptions import ImproperlyConfigured
from starbase.content_types import CONTENT_TYPES_DICT, CONTENT_TYPES, DEFAULT_CONTENT_TYPE
from starbase.defaults import HOST, PORT, USER, PASSWORD, PERFECT_DICT
from starbase.client.table import Table
from starbase.client.transport import HttpRequest

class Connection(object):
    """
    Connection instance.

    :param str host: Stargate host.
    :param int port: Stargate port.
    :param str user: Stargate user. Use this if your stargate is protected with HTTP basic
        auth (to be used in combination with `password` argument).
    :param str password: Stargate password (see comment to `user`).
    :param bool secure: If set to True, HTTPS is used; otherwise - HTTP. Default value is False.
    :param str content_type: Content type for data wrapping when communicating with the
        Stargate. Possible options are: json.
    :param bool perfect_dict: Global setting. If set to True, generally data will be returned as
        perfect dict.
    """
    def __init__(self, host=HOST, port=PORT, user=USER, password=PASSWORD, secure=False, \
                 content_type=DEFAULT_CONTENT_TYPE, perfect_dict=PERFECT_DICT):
        """
        Creates a new connection instance.

        See docs above.
        """
        if not content_type in CONTENT_TYPES:
            raise ImproperlyConfigured(_("Invalid ``content_type`` {0} value.".format(content_type)))

        if not host:
            raise ImproperlyConfigured(_("Invalid ``host`` {0} value.".format(host)))

        if not port:
            raise ImproperlyConfigured(_("Invalid ``port`` {0} value.".format(port)))

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.secure = secure
        self.content_type = CONTENT_TYPES_DICT[content_type]
        self.perfect_dict = perfect_dict
        self.__connect()

    def __repr__(self):
        return "<starbase.client.connection.Connection ({0}:{1})>".format(self.host, self.port)

    def __connect(self):
        data = {
            'secure': 's' if self.secure else '',
            'host': self.host,
            'port': self.port,
            #'user_credentials': ("{0}:{1}@".format(self.user, self.password)) if (self.user and self.password) else ''
        }
        #self.base_url = 'http{secure}://{user_credentials}{host}:{port}/'.format(**data)
        self.base_url = 'http{secure}://{host}:{port}/'.format(**data)

    @property
    def version(self):
        """
        Software version. Returns the software version.

        :return dict: Dictionary with info on software versions (OS, Server, JVM, etc).
        """
        response = HttpRequest(connection=self, url='version').get_response()
        return response.content

    @property
    def cluster_version(self):
        """
        Storage cluster version. Returns version information regarding the HBase cluster backing the Stargate
        instance.

        :return str: HBase version.
        """
        response = HttpRequest(connection=self, url='version/cluster').get_response()
        return response.content

    @property
    def cluster_status(self):
        """
        Storage cluster satus. Returns detailed status on the HBase cluster backing the Stargate instance.

        :return dict: Dictionary with information on dead nodes, live nodes, average load, regions, etc.
        """
        response = HttpRequest(connection=self, url='status/cluster').get_response()
        return response.content

    def table(self, name):
        """
        Initializes a table instance to work with.

        :param str name: Table name. Example value 'test'.
        :return stargate.base.Table:

        .. note::
            This method does not check if table exists. Use the following methods to perform the
            check:

                - `starbase.client.Connection.table_exists` or
                - `starbase.client.table.Table.exists`.
        """
        return Table(connection=self, name=name)

    def tables(self, raw=False):
        """
        Table list. Retrieves the list of available tables.

        :param bool raw: If set to True raw result (JSON) is returned.
        :return list: Just a list of plain strings of table names, no Table instances.
        """
        response = HttpRequest(connection=self).get_response()
        if not raw:
            try:
                return [table['name'] for table in response.content['table']]
            except:
                return []
        return response.content

    def table_exists(self, name):
        """
        Checks if table exists.

        :param str name: Table name.
        :return bool:
        """
        return name in self.tables()

    # ******************** Helper methods ********************
    def create_table(self, name, *columns):
        """
        Creates the table and returns the instance created. If table already exists, returns None.

        :param str name: Table name.
        :param list|tuple *columns:
        :return starbase.client.table.Table:
        """
        assert columns
        table = self.table(name)
        if not table.exists():
            table.create(*columns)
            return table

    def drop_table(self, name):
        """
        Drops the table.

        :param str name: Table name.
        :return int: Status code.
        """
        table = self.table(name)
        return table.drop()
