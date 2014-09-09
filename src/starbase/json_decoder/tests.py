import unittest
import base64

from six import print_

from starbase.json_decoder import json_decode

class Registry(object):
    pass

ordering = []

registry = Registry()

PRINT_INFO = True
TRACK_TIME = False

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):
        if TRACK_TIME:
            import simple_timer
            timer = simple_timer.Timer() # Start timer

        ordering.append(func.__name__)

        result = func(self, *args, **kwargs)

        if TRACK_TIME:
            timer.stop() # Stop timer

        print_('\n\n{0}'.format(func.__name__))
        print_('============================')
        if func.__doc__:
            print_('""" {0} """'.format(func.__doc__.strip()))
        print_('----------------------------')
        if result is not None:
            print_(result)
        if TRACK_TIME:
            print_('done in {0} seconds'.format(timer.duration))
        print_('\n++++++++++++++++++++++++++++')

        return result
    return inner

class JSONDecoderTest(unittest.TestCase):
    """
    JSON deoder tests.
    """
    def setUp(self):
        self.test_encoded_data_1 = {
            'Row': [
                {
                    'Cell': [
                        {'$': 'NDQ=', 'column': 'Y29tcG9uZW50Omlk', 'timestamp': 1369030584274},
                        {'$': 'MQ==', 'column': 'bWFjaGluZTppZA==', 'timestamp': 1369030584274},
                        {'$': 'NTUx', 'column': 'c2Vuc29yOmlk', 'timestamp': 1369030584274},
                        {'$': 'NjQ2', 'column': 'c2Vuc29yOm1lYXN1cmVtZW50', 'timestamp': 1369030584274},
                        {'$': 'VGVtcA==', 'column': 'c2Vuc29yOnR5cGU=', 'timestamp': 1369030584274},
                        {'$': 'UGFzY2Fs', 'column': 'c2Vuc29yOnVuaXRfb2ZfbWVhc3VyZQ==', 'timestamp': 1369030584274}
                    ],
                    'key': 'NDk1MzczYzMtNGVkZi00OWZkLTgwM2YtMDljYjIxYTYyN2Vh'
                }
            ]
        }

        self.test_encoded_data_2 = {
            'Row': [
                {
                    'Cell': [
                        {'column': 'bWFjaGluZTppZA==', 'timestamp': 1369238802349, '$': ''}
                        ],
                    'key': 'cm93XzUyMTZkNTU5LTZmOTUtNDg1NS05OGExLWYyYmQxZDc5Zjg3YzA='
                }
            ]
        }

        self.test_clean_data_1 = {
            'Row': {
                'Cell': [
                    {'@column': 'sensor:id', '$': '345'},
                    {'@column': 'sensor:unit_of_measure', '$': 'dB'},
                    {'@column': 'machine:id', '$': '123'},
                    {'@column': 'component:id', '$': '234'},
                    {'@column': 'sensor:measurement', '$': '123456'}
                ],
            '@key': 'row_a1ed8110-dbca-4093-a447-69157b38dca5'}
            }

        self.test_clean_data_2 = {
            'Row': {
                'Cell': {'@column': 'machine:id', '$': '0'},
                '@key': 'row_e6f61c2f-c30a-4b38-8b68-451c538a0a5b0'
                }
            }

        self.test_clean_data_3 = {
            'Cell': [
                {'@column': 'sensor:id', '$': '345'},
                {'@column': 'sensor:unit_of_measure', '$': 'dB'},
                {'@column': 'machine:id', '$': '123'},
                {'@column': 'component:id', '$': '234'},
                {'@column': 'sensor:measurement', '$': '123456'}],
            '@key': 'row_a1ed8110-dbca-4093-a447-69157b38dca5'
            }

    @print_info
    def __test_01_encode_data(self, test_clean_data):
        """
        Test encode data.
        """
        res = json_decode(test_clean_data, decoder=base64.encodestring)
        self.assertTrue(len(res) == len(test_clean_data))
        return res

    def test_01_1_encode_data(self):
        """
        Test encode data.
        """
        return self.__test_01_encode_data(test_clean_data=self.test_clean_data_1)

    def test_01_2_encode_data(self):
        """
        Test encode data.
        """
        return self.__test_01_encode_data(test_clean_data=self.test_clean_data_2)

    def test_01_3_encode_data(self):
        """
        Test encode data.
        """
        return self.__test_01_encode_data(test_clean_data=self.test_clean_data_3)

    @print_info
    def __test_02_decode_data(self, test_encoded_data):
        """
        Test decode data.
        """
        res = json_decode(test_encoded_data) # , keys_to_bypass_decoding=['timestamp']
        self.assertTrue(len(res) == len(test_encoded_data))
        return res

    def test_02_1_encode_data(self):
        """
        Test encode data.
        """
        return self.__test_02_decode_data(test_encoded_data=self.test_encoded_data_1)

    def test_02_2_encode_data(self):
        """
        Test encode data.
        """
        return self.__test_02_decode_data(test_encoded_data=self.test_encoded_data_2)


if __name__ == '__main__':
    unittest.main()
