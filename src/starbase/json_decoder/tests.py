import base64

from starbase.json_decoder import json_decode

test_encoded_data_1 = {
    u'Row': [
        {
            u'Cell': [
                {u'$': u'NDQ=', u'column': u'Y29tcG9uZW50Omlk', u'timestamp': 1369030584274},
                {u'$': u'MQ==', u'column': u'bWFjaGluZTppZA==', u'timestamp': 1369030584274},
                {u'$': u'NTUx', u'column': u'c2Vuc29yOmlk', u'timestamp': 1369030584274},
                {u'$': u'NjQ2', u'column': u'c2Vuc29yOm1lYXN1cmVtZW50', u'timestamp': 1369030584274},
                {u'$': u'VGVtcA==', u'column': u'c2Vuc29yOnR5cGU=', u'timestamp': 1369030584274},
                {u'$': u'UGFzY2Fs', u'column': u'c2Vuc29yOnVuaXRfb2ZfbWVhc3VyZQ==', u'timestamp': 1369030584274}
            ],
            u'key': u'NDk1MzczYzMtNGVkZi00OWZkLTgwM2YtMDljYjIxYTYyN2Vh'
        }
    ]
}

test_encoded_data_2 = {
    u'Row': [
        {
            u'Cell': [
                {u'column': u'bWFjaGluZTppZA==', u'timestamp': 1369238802349, u'$': u''}
                ],
            u'key': u'cm93XzUyMTZkNTU5LTZmOTUtNDg1NS05OGExLWYyYmQxZDc5Zjg3YzA='
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

print "Encoding data\n================================\n"
print json_decode(test_clean_data_1, decoder=base64.encodestring), '\n'
print json_decode(test_clean_data_2, decoder=base64.encodestring), '\n'
print json_decode(test_clean_data_3, decoder=base64.encodestring), '\n'

print "Decoding data\n================================\n"
print json_decode(test_encoded_data_1), '\n'
print json_decode(test_encoded_data_2), '\n' # , keys_to_bypass_decoding=['timestamp']
