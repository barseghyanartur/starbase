import base64

from six import print_

from starbase.json_decoder import json_decode

test_encoded_data_1 = {
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

test_encoded_data_2 = {
    'Row': [
        {
            'Cell': [
                {'column': 'bWFjaGluZTppZA==', 'timestamp': 1369238802349, '$': ''}
                ],
            'key': 'cm93XzUyMTZkNTU5LTZmOTUtNDg1NS05OGExLWYyYmQxZDc5Zjg3YzA='
        }
    ]
}

test_clean_data_1 = {
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

test_clean_data_2 = {
    'Row': {
        'Cell': {'@column': 'machine:id', '$': '0'},
        '@key': 'row_e6f61c2f-c30a-4b38-8b68-451c538a0a5b0'
        }
    }

test_clean_data_3 = {
    'Cell': [
        {'@column': 'sensor:id', '$': '345'},
        {'@column': 'sensor:unit_of_measure', '$': 'dB'},
        {'@column': 'machine:id', '$': '123'},
        {'@column': 'component:id', '$': '234'},
        {'@column': 'sensor:measurement', '$': '123456'}],
    '@key': 'row_a1ed8110-dbca-4093-a447-69157b38dca5'
    }

print_("Encoding data\n================================\n")
print_(json_decode(test_clean_data_1, decoder=base64.encodestring), '\n')
print_(json_decode(test_clean_data_2, decoder=base64.encodestring), '\n')
print_(json_decode(test_clean_data_3, decoder=base64.encodestring), '\n')

print_("Decoding data\n================================\n")
print_(json_decode(test_encoded_data_1), '\n')
print_(json_decode(test_encoded_data_2), '\n') # , keys_to_bypass_decoding=['timestamp']
