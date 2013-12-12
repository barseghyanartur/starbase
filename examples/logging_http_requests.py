"""
Logging HTTP requests.
"""
import logging

logging.basicConfig(level=logging.DEBUG)

from starbase import Connection

c = Connection()

c.tables()

t = c.table('table4')

t.create('column1', 'column2', 'column3')

t.exists()

t.add_columns('column4', 'column5', 'column6', 'column7')

t.drop_columns('column6', 'column7')

t.insert(
    'my-key-1',
    {
        'column1': {'key11': 'value 11', 'key12': 'value 12',
                    'key13': 'value 13'},
        'column2': {'key21': 'value 21', 'key22': 'value 22'},
        'column3': {'key32': 'value 31', 'key32': 'value 32'}
    }
)

t.update(
    'my-key-1',
    {'column4': {'key41': 'value 41', 'key42': 'value 42'}}
)

t.remove('my-key-1', 'column4', 'key41')

t.remove('my-key-1', 'column4')

t.remove('my-key-1')

t.insert(
    'my-key-1',
    {
        'column1': {'key11': 'value 11', 'key12': 'value 12',
                    'key13': 'value 13'},
        'column2': {'key21': 'value 21', 'key22': 'value 22'},
        'column3': {'key32': 'value 31', 'key32': 'value 32'}
    }
)

t.fetch('my-key-1')

t.fetch('my-key-1', ['column1', 'column2'])

t.fetch('my-key-1', {'column1': ['key11', 'key13'], 'column3': ['key32']})

t.fetch_all_rows()

