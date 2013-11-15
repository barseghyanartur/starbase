__title__ = 'starbase.client.table.__init__'
__author__ = 'Artur Barseghyan'
__all__ = ('Table',)

import base64
import json

from six import string_types, PY3

from starbase.exceptions import InvalidArguments
from starbase.content_types import DEFAULT_CONTENT_TYPE
from starbase.defaults import PERFECT_DICT
from starbase.client.transport import HttpRequest
from starbase.client.transport.methods import GET, PUT, POST, DELETE
from starbase.client.table.scanner import Scanner
from starbase.client.table.batch import Batch
from starbase.client.helpers import build_json_data

class Table(object):
    """
    For HBase table operations.

    :param stargate.base.Connection connection: Connection instance.
    :param str name: Table name.
    """
    FALSE_ROW_KEY = 'false-row-key'

    def __init__(self, connection, name):
        """
        Creates a new table instance.

        See docs above.
        """
        self.connection = connection
        self.name = name

    def __repr__(self):
        return "<starbase.client.table.Table ({0})> on {1}".format(self.name, self.connection)

    @staticmethod
    def _extract_usable_data(data, with_row_id=False, perfect_dict=PERFECT_DICT):
        """
        Extracts usable data from source given. The opposite to ``_build_table_data``.

        :param dict data: Source. For examples see the tests (``test_16a_test_extract_usable_data_as_perfect_dict``).
        :param bool with_row_id: If set to True, row is is aslso returned.
        :param bool perfect_dict: If set to True, returns a perfect dict. If not given, global setting is used.

        :return list|dict: Extracted usable data.
        """
        assert 'Row' in data
        row_data = data['Row']

        assert isinstance(row_data, (list, dict))

        # Single row data
        if isinstance(row_data, dict):
            return Table._extract_row_data(row_data, perfect_dict=perfect_dict, with_row_id=with_row_id)

        # Multiple row data
        else:
            extracted_data = []
            for item in row_data:
                extracted_data.append(Table._extract_row_data(item, perfect_dict=perfect_dict, with_row_id=with_row_id))
            return extracted_data

    @staticmethod
    def _extract_column_data(column_data, perfect_dict=PERFECT_DICT):
        """
        Extracts column data. See doc string of the ``extract_cell_data`` for the data structure types.

        :param dict column_data:
        :param bool perfect_dict: If set to True, returns a perfect dict. If not given, global setting is used.
        :return dict:
        """
        assert 'column' in column_data
        assert '$' in column_data

        if perfect_dict:
            if PY3:
                if isinstance(column_data['column'], bytes):
                    column = column_data['column'].decode('utf8').split(':')
                else:
                    column = column_data['column'].split(':')
            else:
                column = column_data['column'].split(':')

            assert 2 == len(column)
            column_family, key = column
            return {column_family: {key: column_data['$']}}
        else:
            return {column_data['column']: column_data['$']}

    @staticmethod
    def _extract_cell_data(cell_data, perfect_dict=PERFECT_DICT):
        """
        Extracts the cell data.

        :param list|dict cell_data:
        :param bool perfect_dict: If set to True, a perfect dictionary is returned (see data structure #2 and #4).
            Otherwise, ordinary structure is returned (see data structure #1 and #3). If not given, global setting
            is used.
        :return list|dict:
        """
        assert isinstance(cell_data, (list, dict))

        extracted_cell_data = None

        # Single column
        if isinstance(cell_data, dict):
            extracted_cell_data = Table._extract_column_data(cell_data, perfect_dict=perfect_dict)

        # Multiple column
        else:
            if perfect_dict:
                extracted_cell_data = {}
                for column_data in cell_data:
                    d = Table._extract_column_data(column_data, perfect_dict=perfect_dict)
                    for d_key, d_val in d.items():
                        if PY3:
                            if isinstance(d_val, bytes):
                                d_val = d_val.decode('utf8')

                        if d_key in extracted_cell_data:
                            extracted_cell_data[d_key].update(d_val)
                        else:
                            extracted_cell_data[d_key] = d_val
            else:
                extracted_cell_data = {}
                for column_data in cell_data:
                    extracted_cell_data.update(Table._extract_column_data(column_data, perfect_dict=perfect_dict))
        return extracted_cell_data

    @staticmethod
    def _extract_row_data(row_data, with_row_id=False, perfect_dict=PERFECT_DICT):
        """
        See doc string of the ``_extract_usable_data`` for complete data overview.

        :param dict row_data:
        :param bool perfect_dict:  If set to True, returns a perfect dict. If not given, global setting is used.

        :return dict:
        """
        assert 'Cell' in row_data
        assert 'key' in row_data

        result = Table._extract_cell_data(row_data['Cell'], perfect_dict=perfect_dict)
        if with_row_id:
            return {row_data['key']: result}

        return result

    def _build_url_parts(self, columns):
        """
        Builds part of the URL based on the column family data. See ``get`` method for nice examples of the
        ``columns`` values.

        :param list|set|tuple|dict columns:

        :return str:
        """
        # Additional URL parts
        url_parts = []

        # Building additional URL parts.
        if columns:
            if isinstance(columns, (list, tuple, set)):
                for column in columns:
                    url_parts.append(column)
            if isinstance(columns, dict):
                for column, qualifiers in columns.items():
                    for qualifier in qualifiers:
                        url_parts.append('{column}:{qualifier}'.format(column=column, qualifier=qualifier))

        return ','.join(url_parts)

    def _build_table_data(self, row, columns, timestamp=None, encode_content=False,
                          content_type=DEFAULT_CONTENT_TYPE, with_row_declaration=True):
        """
        Builds table data based on row column family data. See ``get`` method for nice examples of the ``columns``
        values.

        Most likely, this is only going to be used for post/put methods.

        :param str row: Example 'row1'.
        :param dict columns: See data structure #1 and data structure #2 further for examples.
        :param timestamp: Not yet used.
        :param bool encode_content: If set to True, table data is encoded with base64.encodestring.
        :param str content_type: Content type. Can be 'json'
        :param bool with_row_declaration: If set to True, {"Row" : [table_data]} structure is returned. Otherwise
            just table_data. False setting is used when preparing data for batch processing. Default value is True.

        :return dict:
        """
        return build_json_data(row, columns, timestamp=timestamp, encode_content=encode_content, \
                               with_row_declaration=with_row_declaration)

    def _get(self, row, columns=None, timestamp=None, decode_content=True, number_of_versions=None, raw=False, \
            perfect_dict=None):
        """
        Retrieves one or more cells from a full row, or one or more specified columns in the row, with optional
        filtering via timestamp, and an optional restriction on the maximum number of versions to return.

        The `raw` argument is dominant. If given, the raw response it returned. Otherwise, a nice response is
        returned that does make sense. If `perfect_dict` set to True, then we return a nice dict, instead of a
        horrible one.

        In result JSON, the value of the `$` field (key) is the cell data.

        :param str row:
        :param list|set|tuple|dict columns:
        :param timestamp: Not yet used.
        :param bool decode_content: If set to True, content is decoded using ``stargate.json_decoder.json_decode``.
        :param int number_of_versions: If provided, multiple versions of the given record are returned.
        :param bool perfect_dict:
        :param bool raw:
        :return dict:
        """
        if not self.exists():
            return None

        if perfect_dict is None:
            perfect_dict = self.connection.perfect_dict

        # If just one column given as string, make a list of it.
        if isinstance(columns, string_types):
            columns = [columns]

        # Base URL
        url = "{table_name}/{row}/".format(table_name=self.name, row=row)

        url += self._build_url_parts(columns)

        # If should be versioned, adding additional URL parts.
        if number_of_versions is not None:
            assert isinstance(number_of_versions, int)
            url += '?v={0}'.format(str(number_of_versions))
        response = HttpRequest(connection=self.connection, url=url, decode_content=decode_content).get_response()

        response_content = response.content

        if raw:
            return response_content

        if response_content:
            try:
                res = Table._extract_usable_data(response_content, perfect_dict=perfect_dict, with_row_id=False)
                if isinstance(res, (list, tuple)) and 1 == len(res):
                    return res[0]
            except:
                pass

    def fetch(self, row, columns=None, timestamp=None, number_of_versions=None, raw=False, perfect_dict=None):
        """
        Fetches a single row from table.

        :param str row:
        :param list|set|tuple|dict columns:
        :param timestamp: Not yet used.
        :param int number_of_versions: If provided, multiple versions of the given record are returned.
        :param bool perfect_dict:
        :param bool raw:
        :return dict:

        :example:
        In the example below we first create a table named `table1` with columns `column1`, `column2` and
        `column3`, then insert a row with `column1` and `column2` data, then update the same row with
        `column3` data and then fetch the data.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.create('column1', 'column2', 'column3')
        >>> table.insert('row1', {'column1': {'id': '1', 'name': 'Some name'}, 'column2': {'id': '2', 'age': '32'}})
        >>> table.update('row2', {'column3': {'gender': 'male', 'favourite_book': 'Steppenwolf', 'active': '1'}})

        Fetching entire `row1`.

        >>> table.fetch('row1')

        Fetching the row `row1` with data from `column1` and `column3` only.

        >>> table.fetch('row1', ['column1', 'column3'])

        Fetching the row `row1` with fields `gender` and `favourite_book` from `column3` and fild `age` of column
        `column2`.

        >>> table.fetch('row1', {'column3': ['gender', 'favourite_book'], 'column2': ['age']})
        """
        return self._get(row, columns=columns, timestamp=timestamp, decode_content=True, \
                         number_of_versions=number_of_versions, raw=False, perfect_dict=perfect_dict)

    def fetch_all_rows(self, with_row_id=False, raw=False, perfect_dict=None, flat=False, filter_string=None, scanner_config=''):
        """
        Fetches all table rows.

        :param bool with_row_id: If set to True, returned along with row id.
        :param bool raw: If set to True, raw response is returned.
        :param bool perfect_dict: If set to True, a perfect dict struture is used for output data.
        :param string filter_string: If set, applies the given filter string to the scanner.
        :returns list:

        :example:
        >>> filter_string = '{"type": "RowFilter", "op": "EQUAL", "comparator": '
        >>>                 '{"type": "RegexStringComparator", "value": "^row_1.+"}}'
        >>> rows = self.table.fetch_all_rows(
        >>>            with_row_id = True,
        >>>            perfect_dict = perfect_dict,
        >>>            filter_string = row_filter_string
        >>>            )
        """
        if not self.exists():
            return None

        if perfect_dict is None:
            perfect_dict = self.connection.perfect_dict

        scanner = self._scanner(filter_string=filter_string, data=scanner_config)
        res = scanner.results(perfect_dict=perfect_dict, with_row_id=with_row_id, raw=raw)
        scanner.delete ()

        if flat:
            res = list(res)

        return res

    def _build_put_url(self, row, columns):
        """
        Builds a URL to use for sending the PUT/POST commands.

        :param str row:
        :param dict columns:
        :return str:
        """
        # Base URL
        url = ''

        if PY3:
            row_hash = base64.b64encode(row.encode('utf8')).decode('utf8')
        else:
            row_hash = base64.b64encode(row)

        if 1 == len(columns):
            cf = list(columns.keys())[0]
            url = "{table_name}/{row}/{cf}".format(table_name=self.name, row=row_hash, cf=cf)
        else:
            url = "{table_name}/{row}".format(table_name=self.name, row=row_hash)

        return url
    _build_post_url = _build_put_url
    _build_post_url.__doc__ = _build_put_url.__doc__

    def _build_delete_url(self, row, column=None, qualifier=None):
        """
        Builds a URL to use for sending the DELETE commands.

        :param str row: Row id to delete.
        :param str column: Column
        :param str qualifier: Column qualifier.
        :return str:
        """
        if qualifier and not column:
            raise InvalidArguments(_("Qualifier can't be given without column."))

        # Base URL
        parts = []
        parts.append("{table_name}/{row}".format(table_name=self.name, row=row))

        if qualifier:
            parts.append("{0}:{1}".format(column, qualifier))
        elif column:
            parts.append("{0}".format(column))

        return '/'.join(parts)

    def _put(self, row, columns, timestamp=None, encode_content=True):
        """
        Cell store (single or multiple). If not successful, returns appropriate HTTP error status code. If
        successful, returns HTTP 200 status.

        ..note: Inserting of multiple rows could be achieved with batch.

        :param str row:
        :param dict columns:
        :param bool encode_content: Better be True, because otherwise values may not be submitted correctly.
        :return int:
        """
        if not self.exists():
            return None

        url = self._build_put_url(row, columns)

        data = self._build_table_data(row, columns, timestamp=timestamp, encode_content=encode_content, \
                                      with_row_declaration=True)

        response = HttpRequest(
            connection = self.connection,
            url = url,
            data = data,
            decode_content = False,
            method = PUT
            ).get_response()

        return response.status_code

    def insert(self, row, columns, timestamp=None):
        """
        Inserts a single row into a table.

        :param str row:
        :param (list, tuple or set) columns:
        :param timestamp:
        :return int: HTTP status code (200 on success).

        :example:
        In the example below we first create a table named `table1` and then insert two rows to it.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.create('column1', 'column2', 'column3')
        >>> table.insert('row1', {'column1': {'id': '1', 'name': 'Some name'}, 'column2': {'id': '2', 'age': '32'}})
        >>> table.insert('row2', {'column3': {'gender': 'male', 'favourite_book': 'Steppenwolf'}})
        """
        return self._put(row=row, columns=columns, timestamp=timestamp)

    def _scanner(self, batch_size=None, start_row=None, end_row=None, start_time=None, end_time=None, \
                 filter_string=None, data=''):
        """
        Creates a scanner instance.

        :param int batch_size:
        :param str start_row:
        :param str end_row:
        :param start_time:
        :param end_time:
        :param str filter_string:
        :return starbase.client.Scanner: Creates and returns a class::`starbase.client.Scanner` instance.
        """
        url = '{0}/scanner'.format(self.name)

        if filter_string is not None:
            data = {"filter": filter_string}

        response = HttpRequest(connection=self.connection, url=url, data=data, method=PUT).get_response()
        scanner_url = response.raw.headers.get('location')

        return Scanner(table=self, url=scanner_url)

    def _post(self, row, columns, timestamp=None, encode_content=True):
        """
        Update (POST) operation.

        :param str:
        :param dict columns:
        :param timestamp: Not yet used.
        :param bool encode_content: Better be True, because otherwise values may not be submitted correctly.
        :return int:
        """
        if not self.exists():
            return None

        url = self._build_put_url(row, columns)

        data = self._build_table_data(row, columns, timestamp=timestamp, encode_content=encode_content, \
                                      with_row_declaration=True)

        response = HttpRequest(
            connection = self.connection,
            url = url,
            data = data,
            decode_content = False,
            method = POST
            ).get_response()

        return response.status_code

    def update(self, row, columns, timestamp=None):
        """
        Updates a single row in a table.

        :param str row:
        :param dict columns:
        :param timestamp: Not yet used.
        :return int: HTTP response status code (200 on success).

        :example:
        In the example below we first create a table named `table1` with columns `column1`, `column2` and
        `column3`. Then we insert a row with `column1` and `column2` data and then update the same row with
        `column3` data.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.create('column1', 'column2', 'column3')
        >>> table.insert('row1', {'column1': {'id': '1', 'name': 'Some name'}, 'column2': {'id': '2', 'age': '32'}})
        >>> table.update('row1', {'column3': {'gender': 'female', 'favourite_book': 'Solaris'}})
        """
        return self._post(row, columns, timestamp=timestamp)

    def drop(self):
        """
        Drops current table. If not successful, returns appropriate HTTP error status code. If successful,
        returns HTTP 200 status.

        :return int: HTTP response status code (200 on success).

        :example:
        In the example below we check if table named `table1` exists and if so - drop it.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> if table.exists():
        >>>     table.drop()
        """
        response = HttpRequest(
            connection = self.connection,
            url = '{0}/schema'.format(self.name),
            method = DELETE
            ).get_response()

        # If response.status_code == 200 it means table was successfully dropped/deleted.
        return response.status_code

    def _delete(self, row, column=None, qualifier=None, timestamp=None):
        """
        Deletes the table row or selected columns row given. If not successful, returns appropriate HTTP error
        status code. If successful, returns HTTP 200 status.

        :param str row: Row id to delete.
        :param str column: Column to delete. If given, only that specific column is deleted. If left blank or
            set to None, entire row is deleted.
        :param str qualifier: Column qualifier. If given, only that specific column qualifier is deleted. If left
            blank or set to None, entire column family is deleted.
        :return int: HTTP status code.
        """
        url = self._build_delete_url(row=row, column=column, qualifier=qualifier)

        response = HttpRequest(connection=self.connection, url=url, method=DELETE).get_response()
        return response.status_code

    def remove(self, row, column=None, qualifier=None, timestamp=None):
        """
        Removes/delets a single row/column/qualifier from a table (depending on the depth given). If only row
        is given, the entire row is deleted. If row and column, only the column value is deleted (entirely for
        the row given). If qualifier is given as well, then only the qualifier value would be deleted.

        :param str row:
        :param str column:
        :param str qualifier:
        :return int: HTTP status code.

        :example:
        In the example below we first create a table named `table1` with columns `column1`, `column2` and
        `column3`. Then we insert a single row with multiple columns and then remove parts from that row.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.create('column1', 'column2', 'column3')
        >>> table.insert('row1', {'column1': {'id': '1', 'name': 'Some name'}, 'column2': {'id': '2', 'age': '32'}})
        >>> table.remove('row1', 'column2', 'id')
        >>> table.remove('row1', 'column1')
        >>> table.remove('row1')
        """
        return self._delete(row, column=column, qualifier=qualifier, timestamp=timestamp)

    def schema(self):
        """
        Table schema. Retrieves table schema.

        :return dict: Dictionary with schema info (detailed information on column families).

        :example:
        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.schema()
        """
        url = "{table_name}/schema".format(table_name=self.name)
        response = HttpRequest(connection=self.connection, url=url).get_response()
        return response.content

    def exists(self):
        """
        Checks if table exists.

        :return bool:

        :example:
        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.exists()
        """
        return self.connection.table_exists(self.name)

    def columns(self):
        """
        Gets a plain list of column families of the table given.

        :return list: Just a list of plain strings of column family names.

        :example:
        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.columns()
        """
        schema = self.schema()
        columns_schema = schema['ColumnSchema'] if schema and 'ColumnSchema' in schema else []

        return [cf['name'] for cf in columns_schema]

    def regions(self):
        """
        Table metadata. Retrieves table region metadata.

        :return dict:
        """
        url = "{table_name}/regions".format(table_name=self.name)
        response = HttpRequest(connection=self.connection, url=url).get_response()
        return response.content
    metadata = regions
    metadata.__doc__ = regions.__doc__

    def create(self, *columns):
        """
        Creates a table schema. If not successful, returns appropriate HTTP error status code. If successful,
        returns HTTP 201 status.

        :param list *columns: List of columns (plain strins).
        :return int: HTTP response status code (201 on success). Returns boolean False on failure.

        :example:
        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.create('column1', 'column2')
        """
        # If table exists, return False
        if self.exists():
            return False

        url, data = self._get_data_for_table_create_or_update(columns)

        response = HttpRequest(connection=self.connection, url=url, data=data, method=PUT).get_response()
        return response.status_code

    def _get_data_for_table_create_or_update(self, columns):
        """
        Gets data for table create or update.

        :param list|tuple|set|str columns: Columns to (re)create/update.
        :return dict:
        """
        # If just one column given as string, make a list of it.
        if isinstance(columns, string_types):
            columns = [columns]

        columns = set(columns)

        url = "{table_name}/schema".format(table_name=self.name)

        data = {'name': self.name, 'ColumnSchema': []}

        for column in columns:
            data['ColumnSchema'].append({'name': column})

        return url, data

    def _update_schema(self, columns, method=None):
        """
        Updates current table schema. If not successful, returns appropriate HTTP error status code. If
        successful, returns HTTP 200 status or boolean False if table does not exist.

        :param list columns: List of columns (plain strins).
        :param str method: HTTP method (GET, POST, PUT, DELETE).
        :return int: HTTP response status code.
        """
        if not self.exists():
            return False

        if method is None:
            method = POST

        url, data = self._get_data_for_table_create_or_update(columns)

        response = HttpRequest(connection=self.connection, url=url, data=data, method=method).get_response()
        return response.status_code

    def _replace_schema(self, columns):
        """
        Replaces the table schema.

        :param list columns: List of columns (plain strins). If not successful, returns appropriate HTTP error
            status code. If successful, returns HTTP 200 status or boolean False if table does not exist.
        :return int: HTTP response status code.
        """
        return self._update_schema(columns, method=PUT)

    def add_columns(self, *columns):
        """
        Add columns to existing table (POST). If not successful, returns appropriate HTTP error status code. If
        successful, returns HTTP 200 status.

        :param str name: Table name.
        :param list *columns: List of columns (plain strins) to ADD.
        :return int: HTTP response status code (200 on success).

        :example:
        In the example below we create a new table named `table1` with columns `column1` and `column2`. In the next
        step we add columns `column3` and `columns4` to it.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.create('column1', 'column2')
        >>> table.add_columns('column3', 'column4')
        """
        # If just one column given as string, make a list of it.
        return self._update_schema(columns)

    def drop_columns(self, *columns):
        """
        Removes/drops columns from table (PUT).If not successful, returns appropriate HTTP error status code. If
        successful, returns HTTP 201 status.

        :param str name: Table name.
        :param list *columns: List of columns (plain strins) to REMOVE.
        :return int: HTTP response status code (201 on success).

        :example:
        Assuming that we have a table named `table1` with columns `column1` and `column2`.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> table.drop_columns('column1', 'column2')
        """
        # If just one column given as string, make a list of it.

        columns = set(columns)
        existing_columns = set(self.columns())
        remaining_columns = existing_columns - columns

        return self._replace_schema(remaining_columns)

    def batch(self, size=None):
        """
        Returns a Batch instance. Returns None if table does not exist.

        :param int size: Size of auto-commit. If not given, auto-commit is disabled.
        :return starbase.client.table.batch.Batch:

        :example:
        Assuming that we have a table named `table1` with columns `column1` and `column2`.

        >>> from starbase import Connection
        >>> connection = Connection()
        >>> table = connection.table('table1')
        >>> batch = table.batch()
        >>> batch.insert('row1', {'column1': {'id': '1', 'name': 'Some name'}, 'column2': {'id': '2', 'age': '32'}})
        >>> batch.insert('row2', {'column1': {'id': '12', 'name': 'Some name'}, 'column2': {'id': '22', 'age': '322'}})
        >>> batch.insert('row3', {'column1': {'id': '13', 'name': 'Some name'}, 'column2': {'id': '23', 'age': '323'}})
        >>> batch.commit(finalize=True)
        """
        if not self.exists():
            return None

        return Batch(table=self, size=size)
