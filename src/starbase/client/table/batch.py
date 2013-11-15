__title__ = 'starbase.client.table.batch'
__author__ = 'Artur Barseghyan'
__all__ = ('Batch',)

from starbase.client.transport import HttpRequest
from starbase.client.transport.methods import PUT, POST

class Batch(object):
    """
    Table batch operations.

    :param starbase.client.table.Table table:
    :param int size: Batch size. When set, auto commits stacked records when the stack reaches the
        ``size`` value.
    """
    def __init__(self, table, size=None):
        """
        Creates a new batch instance.

        See docs above.
        """
        self.table = table
        self.size = size
        self._stack = []
        self._url = None
        self._method = None
        self._response = []

    def __repr__(self):
        return "<starbase.client.batch.Batch> of {0}".format(self.table)

    def _put(self, row, columns, timestamp=None, encode_content=True):
        """
        PUT operation in batch.
        """

        if not self._url:
            self._url = self.table._build_put_url(row, columns)

        if not self._method:
            self._method = PUT

        data = self.table._build_table_data(
            row,
            columns,
            timestamp = timestamp,
            encode_content = encode_content,
            with_row_declaration=False
            )

        self._stack.append(data)

        if self.size and len(self._stack) > self.size:
            self.commit()

    def insert(self, row, columns, timestamp=None):
        return self._put(row, columns, timestamp=timestamp, encode_content=True)

    def _post(self, row, columns, timestamp=None, encode_content=True):
        """
        POST operation in batch.
        """
        if not self._url:
            self._url = self.table._build_post_url(row, columns)

        if not self._method:
            self._method = POST

        data = self.table._build_table_data(
            row,
            columns,
            timestamp = timestamp,
            encode_content = encode_content,
            with_row_declaration = False
            )

        self._stack.append(data)

        if self.size and len(self._stack) > self.size:
            self.commit()

    def update(self, row, columns, timestamp=None, encode_content=True):
        return self._post(row, columns, timestamp=timestamp)

    def commit(self, finalize=False):
        """
        Sends all queued items to Stargate.

        :param bool finalize: If set to True, the batch is finalized, settings are cleared up and response is
            returned.

        :return dict: If `finalize` set to True, returns the returned value of method
            meth::`starbase.client.batch.Batch.finalize`.
        """
        response = HttpRequest(
            connection = self.table.connection,
            url = self._url,
            data = {"Row" : self._stack},
            decode_content = False,
            method = self._method,
            ).get_response()
        self._response.append(response.status_code)
        self._stack = []

        if finalize:
            return self.finalize()

    def finalize(self):
        """
        Finalize the batch operation. Clear all settings.

        :return dict:
        """
        response = {
            'url': self._url,
            'method': self._method,
            'response': self._response
        }
        self._url = None
        self._method = None
        self._response = []
        return response

    def outgoing(self):
        """
        Returns number of outgoing requests.

        :return int:
        """
        return len(self._stack)
