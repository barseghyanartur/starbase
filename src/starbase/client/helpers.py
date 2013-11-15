__title__ = 'starbase.client.helpers'
__author__ = 'Artur Barseghyan'
__all__ = ('build_json_data',)

import base64

from six import PY3

# Importing OrderedDict with fallback to separate package for Python 2.6 support.
try:
    from collections import OrderedDict
except ImportError as e:
    from ordereddict import OrderedDict

def build_json_data(row, columns, timestamp=None, encode_content=False, with_row_declaration=True):
    """
    Builds JSON data for read-write purposes. Used in `starbase.client.Table._build_table_data`.

    :param str row:
    :param dict columns:
    :param timestamp: Not yet used.
    :param bool encode_content:
    :param bool with_row_declaration:
    :return dict:
    """
    # Encoding the key if necessary
    if encode_content:
        if PY3:
            row = base64.b64encode(row.encode('utf8')).decode('utf8')
        else:
            row = base64.b64encode(row)

    cell = []

    columns_keys = [k for k, v in columns.items()]

    # Building table data dictionary.
    if columns:
        # Data structure #1
        if ':' in columns_keys[0]:
            # Single column case
            if 1 == len(columns):
                key, value = list(columns.items())[0]

                if encode_content:
                    if PY3:
                        key = base64.b64encode(key.encode('utf8')).decode('utf8')
                        value = base64.b64encode(str(value).encode('utf8')).decode('utf8')
                    else:
                        key = base64.b64encode(key)
                        value = base64.b64encode(str(value))

                cell_data = {
                    "column": key,
                    "$": value
                }
                if timestamp:
                    cell_data.update({'timestamp': timestamp})

                cell.append(cell_data)

            # Multi-column case
            else:
                for column in columns.items():
                    key, value = column

                    if encode_content:
                        if PY3:
                            key = base64.b64encode(key.encode('utf8')).decode('utf8')
                            value = base64.b64encode(str(value).encode('utf8')).decode('utf8')
                        else:
                            key = base64.b64encode(key)
                            value = base64.b64encode(str(value))

                    cell_data = {
                        "column": key,
                        "$": value
                    }

                    if timestamp:
                        cell_data.update({'timestamp': timestamp})

                    cell.append(cell_data)

        # Data structure #2. Here we have multi-column cases only and you're advised to make profit of it.
        else:
            for column, data in columns.items():
                for key, value in data.items():
                    column_family = '{0}:{1}'.format(column, key)

                    if encode_content:
                        if PY3:
                            column_family = base64.b64encode(column_family.encode('utf8')).decode('utf8')
                            value = base64.b64encode(str(value).encode('utf8')).decode('utf8')
                        else:
                            column_family = base64.b64encode(column_family)
                            value = base64.b64encode(str(value))

                    cell_data = {
                        "column": column_family,
                        "$": value
                    }

                    if timestamp:
                        cell_data.update({'timestamp': timestamp})

                    cell.append(cell_data)

    table_data = OrderedDict([
        ("key", row),
        ("Cell", cell)
    ])

    if with_row_declaration:
        return {"Row" : [table_data]}
    else:
        return table_data
