__title__ = 'starbase.client.table.scanner'
__author__ = 'Artur Barseghyan'
__all__ = ('Scanner',)

import base64

from starbase.json_decoder import json_decode
from starbase.client.transport import HttpRequest
from starbase.client.transport.methods import PUT, POST, GET, DELETE

class Scanner(object):
    """
    Table scanner operations.
    """
    def __init__(self, table, url, batch_size=None, start_row=None, end_row=None, start_time=None, end_time=None, \
                 data={}, extra_headers={}, method=None):
        self.table = table
        self.url = url
        self.batch_size = batch_size
        self.start_row = start_row
        self.end_row = end_row
        self.start_time = start_time
        self.end_time = end_time
        self.id = url.split('/')[-1]
        url = '{table_name}/scanner/{scanner_id}'.format(table_name=self.table.name, scanner_id=self.id)

        def encode_data(data):
            encoded = {}
            for key, value in data.items():
                encoded.update({base64.b64encode(key): base64.b64encode(value)})
            return encoded

        self.response = HttpRequest(
            connection = self.table.connection,
            url = url,
            data = encode_data(data),
            #extra_headers = extra_headers,
            #method = method
            ).get_response()

    def delete(self):
        """
        Delete scanner.
        """
        url = '{table_name}/scanner/{scanner_id}'.format(table_name=self.table.name, scanner_id=self.id)
        response = HttpRequest(connection=self.table.connection, url=url, method=DELETE).get_response()
        return response.status_code

    def results(self, with_row_id=False, raw=False, perfect_dict=None):
        results = self.response.content

        if perfect_dict is None:
            perfect_dict = self.table.connection.perfect_dict

        if results and results['Row']:
            for item in results['Row']:
                if raw:
                    yield json_decode(item)
                yield self.table.__class__._extract_row_data(
                    json_decode(item),
                    perfect_dict = perfect_dict,
                    with_row_id=with_row_id
                    )

        #for item in self.response.content:
        #    yield item
