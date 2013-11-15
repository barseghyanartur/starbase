__title__ = 'starbase.client.transport.__init__'
__author__ = 'Artur Barseghyan'
__all__ = ('HttpRequest', 'HttpResponse')

import json
import requests
from requests.auth import HTTPBasicAuth

from six import string_types

from starbase.json_decoder import json_decode
from starbase.content_types import MEDIA_TYPE_JSON
from starbase.client.transport.methods import GET, PUT, POST, DELETE, METHODS, DEFAULT_METHOD

class HttpResponse(object):
    """
    HTTP response.

    :param content:
    :param bool raw:
    """
    def __init__(self, content, raw):
        """
        See the docs above.
        """
        self.content = content
        self.raw = raw

    @property
    def status_code(self):
        """
        Gets the HTTP code.

        :return str:
        """
        try:
            return self.raw.status_code
        except:
            return self.raw.code

    def get_content(self, decode_content=False, keys_to_bypass_decoding=[], keys_to_skip=[]):
        """
        Gets response content.

        :param bool decode_content: If set to True, content is decoded with default decoder, having
            the empty keys ignored.
        :param list|tuple|set keys_to_bypass_decoding: List of keys to bypass decoding.
        :param list|tuple|set keys_to_skip: List of keys to ignore (won't be in the resulted content).
        :return str:
        """
        if self.code == 200: # TODO - is it?
            if decode_content:
                return json_decode(
                    self.content,
                    keys_to_bypass_decoding = keys_to_bypass_decoding,
                    keys_to_skip = keys_to_skip
                    )
            else:
                return self.content


class HttpRequest(object):
    """
    HTTP request.

    :param starbase.client.connection.Connection connection:
    :param str url:
    :param dict data:
    :param bool decode_content: If set to True, response content is decoded.
    :param str method:
    """
    def __init__(self, connection, url='', data={}, decode_content=False, method=DEFAULT_METHOD):
        """
        See the docs above.
        """
        assert method in METHODS

        self.__connection = connection
        self.url = url
        self.data = data
        self.decode_content = decode_content
        headers = {
            'Accept': str(self.__connection.content_type),
            'Content-type': str(self.__connection.content_type) + '; charset=UTF-8'
            }
        endpoint_url = self.__connection.base_url + self.url

        is_xml_request = False
        if isinstance(self.data, string_types) and self.data[:1] == '<':
            is_xml_request = True

        if is_xml_request:
            headers['Content-type'] = 'text/xml'
        else:
            data = json.dumps(data)

        request_data = {
            'url': endpoint_url,
            'headers': headers
        }

        if DELETE != method:
            request_data['data'] = data

        if self.__connection.user and self.__connection.password:
            request_data['auth'] = HTTPBasicAuth(self.__connection.user, self.__connection.password)

        # For the sake of simplicity the `requests` library replaced the `urllib2`.
        if GET == method:
            self.response = requests.get(**request_data)
        elif PUT == method:
            self.response = requests.put(**request_data)
        elif POST == method:
            self.response = requests.post(**request_data)
        elif DELETE == method:
            self.response = requests.delete(**request_data)

    def get_response(self):
        """
        :return starbase.client.transport.HttpResponse:
        """
        response_content = None

        response_raw = self.response

        if self.__connection.content_type == MEDIA_TYPE_JSON:
            try:
                response_content = self.response.json()
            except ValueError as e:
                response_content = None
            except Exception as e:
                pass
        else:
            raise NotImplementedError("Connection type {0} is not implemented.".format(
                self.__connection.content_type
                ))

        if self.decode_content and self.response.ok: # Make sure OK is ok.
            response_content = json_decode(response_content)

        return HttpResponse(response_content, response_raw)
