"""
Recursively decodes values of entire dictionary (JSON) using `base64.decodestring`. Optionally ignores keys
given in `keys_to_skip`. It's also possible to give a custom `decoder` instead of `base64.decodestring`.
"""

__title__ = 'starbase.json_decoder'
__author__ = 'Artur Barseghyan'
__all__ = ('json_decode',)

from six import PY3
from six import string_types
import base64

DEBUG = False

def json_decode(json_data, keys_to_bypass_decoding=['timestamp'], keys_to_skip=[], decoder=base64.decodestring):
    """
    Recursively decodes values of entire dictionary (JSON) using `base64.decodestring`. Optionally ignores (does not
    include in the final dictionary) keys given in `keys_to_skip`.

    NOTE: Whenever you can, give `decoder` callables, instead of strings (works faster).

    NOTE: In HBase stargate `$` keys represent values of the columns.

    :param dict json_data:
    :param list|tuple|set keys_to_bypass_decoding: Keys to bypass encoding/decoding. Example value ['timestamp',]
    :param list|tuple|set keys_to_skip: Keys to be excluded from final dict. Example value ['timestamp',]
    :param str decoder: Example value 'base64.decodestring' or base64.decodestring (assuming that `base64` module
        has already been imported).
    :return dict:

    :example 1:
    >>> test_json_data = {
    >>>     u'Row': [
    >>>         {
    >>>             u'Cell': [
    >>>                 {u'$': u'NDQ=', u'column': u'Y29tcG9uZW50Omlk', u'timestamp': 1369030584274},
    >>>                 {u'$': u'MQ==', u'column': u'bWFjaGluZTppZA==', u'timestamp': 1369030584274},
    >>>                 {u'$': u'NTUx', u'column': u'c2Vuc29yOmlk', u'timestamp': 1369030584274},
    >>>                 {u'$': u'NjQ2', u'column': u'c2Vuc29yOm1lYXN1cmVtZW50', u'timestamp': 1369030584274},
    >>>                 {u'$': u'VGVtcA==', u'column': u'c2Vuc29yOnR5cGU=', u'timestamp': 1369030584274},
    >>>                 {u'$': u'UGFzY2Fs', u'column': u'c2Vuc29yOnVuaXRfb2ZfbWVhc3VyZQ==', u'timestamp': 1369030584274}
    >>>             ],
    >>>             u'key': u'NDk1MzczYzMtNGVkZi00OWZkLTgwM2YtMDljYjIxYTYyN2Vh'
    >>>         }
    >>>     ]
    >>> }
    >>> json_decode(test_json_data, keys_to_skip=['timestamp'])

    {
        u'Row': [
            {
                u'Cell': [
                    {u'column': 'component:id'},
                    {u'column': 'machine:id'},
                    {u'column': 'sensor:id'},
                    {u'column': 'sensor:measurement'},
                    {u'column': 'sensor:type'},
                    {u'column': 'sensor:unit_of_measure'}
                ],
                u'key': '495373c3-4edf-49fd-803f-09cb21a627ea'
            }
        ]
    }

    :example 2:
    >>> # Assuming the `test_json_data` is the same as in example 1
    >>> json_decode(test_json_data, decoder='path.to.your.own.decoder')

    :example 3:
    >>> # Assuming the `test_json_data` is the same as in example 1
    >>> json_decode(test_json_data)

    {
        u'Row': [
            {
                u'Cell': [
                    {u'$': '44', u'column': 'component:id'},
                    {u'$': '1', u'column': 'machine:id'},
                    {u'$': '551', u'column': 'sensor:id'},
                    {u'$': '646', u'column': 'sensor:measurement'},
                    {u'$': 'Temp', u'column': 'sensor:type'},
                    {u'$': 'Pascal', u'column': 'sensor:unit_of_measure'}
                ],
                u'key': '495373c3-4edf-49fd-803f-09cb21a627ea'
            }
        ]
    }
    """
    assert isinstance(decoder, string_types) or callable(decoder)

    # Dynamic import in case if given as a string.
    if isinstance(decoder, string_types):
        decoder_function_path_parts = decoder.split('.')

        assert len(decoder_function_path_parts) > 1

        module_path = '.'.join(decoder_function_path_parts[:-1])
        function_name = decoder_function_path_parts[-1]

        exec('from {0} import {1} as decoder'.format(module_path, function_name))
        assert callable(decoder)

    # Final dict
    decoded_json_data = {}

    assert isinstance(json_data, dict)
    assert isinstance(keys_to_bypass_decoding, (list, tuple, set))
    assert isinstance(keys_to_skip, (list, tuple, set))

    # Iterating through keys and values. If value is a string, we decode it using the given `decoder`. Otherwise,
    # if list, tuple or set is given, iterate through the list and recursively call `json_decode` on each child item.
    for key, value in json_data.items():
        if key not in keys_to_skip:
            # Making sure nothing breaks if we get integers or floats.
            if isinstance(value, (int, float)):
                value = str(value)
                # When decoding (really decoding and not encoding) we sometimes deal with integers or floats in the
                # JSON given. In order to have those values encoded too, we encode them to strings, but then also
                # add to the list of keys to bypass decoding, because integers and floats can't be decoded.
                keys_to_bypass_decoding.append(key)

            # If value is a string, we just encode it.
            if isinstance(value, string_types):
                if key not in keys_to_bypass_decoding:
                    if PY3:
                        decoded_json_data.update({key: decoder(value.encode('utf8')).decode('utf8')})
                    else:
                        decoded_json_data.update({key: decoder(value)})
                else:
                    decoded_json_data.update({key: value})
            # If a list, we recursively apply `json_decoder` to all of its' children.
            elif isinstance(value, list):
                decoded_json_data.update({key: []})
                for item in value:
                    decoded_json_data[key].append(json_decode(
                        item,
                        keys_to_bypass_decoding = keys_to_bypass_decoding,
                        keys_to_skip = keys_to_skip,
                        decoder = decoder
                        ))
            # If a dicionary, we treat is a new `json_data` and apply `json_decoder` to it.
            elif isinstance(value, dict):
                decoded_json_data[key] = json_decode(
                    value,
                    keys_to_bypass_decoding = keys_to_bypass_decoding,
                    keys_to_skip = keys_to_skip,
                    decoder = decoder
                    )
            # Otherwise, it's not a valid JSON provided.
            else:
                raise ValueError("Not allowed type for JSON dictionary: {0}".format(type(value)))

    return decoded_json_data
