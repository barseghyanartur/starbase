=========================================
starbase
=========================================
HBase Stargate (REST API) client wrapper for Python.

Read the official documentation of Stargate (http://wiki.apache.org/hadoop/Hbase/Stargate).

Description
=========================================
starbase is (at the moment) a client implementation of the Apache HBase REST API (Stargate).

What you have to know
=========================================
Beware, that REST API is slow (not to blame on this library!). If you can operate with HBase directly
better do so.

Prerequisites
=========================================
You need to have Hadoop, HBase, Thrift and Stargate running. If you want to make it easy for yourself,
read my instructions on installing Cloudera manager (free) on Ubuntu 12.04 LTS here
(http://barseghyanartur.blogspot.nl/2013/08/installing-cloudera-on-ubuntu-1204.html) or
(https://bitbucket.org/barseghyanartur/simple-cloudera-install).

Once you have everything installed and running (by default Stargate runs on 127.0.0.1:8000), you should be able
to run `src/starbase/client/test.py` without problems (UnitTest).

Features
=========================================
Project is still in development, thus not all the features of the API are available.

Features implemented
-----------------------------------------
- Connect to Stargate.
- Show software version.
- Show cluster version.
- Show cluster status.
- List tables.
- Retrieve table schema.
- Retrieve table meta data.
- Get a list of tables' column families.
- Create a table.
- Delete a table.
- Alter table schema.
- Insert (PUT) data into a single row (single or multiple columns).
- Update (POST) data of a single row (single or multiple columns).
- Select (GET) a single row from table, optionally with selected columns only.
- Delete (DELETE) a single row by id.
- Batch insert (PUT).
- Batch update (POST).
- Basic HTTP auth is working. You could provide a login and a password to the connection.
- Retrive all rows in a table (table scanning).

Features in-development
-----------------------------------------
- Table scanning.
- Syntax globbing.

Installation
=========================================
Install latest stable version from PyPi

    $ pip install starbase

Usage examples
=========================================
A lot of useful examples with comments could be found in `stargate.client.tests` module. Some most
common operations are shown below.

Required imports
-----------------------------------------
>>> from starbase import Connection

Create a connection instance
-----------------------------------------
Defaults to 127.0.0.1:8000. Specify when creating a connection instance if your defaults are different.

>>> c = Connection()

Show tables
-----------------------------------------
Assuming that we have two tables named ``table1`` and ``table2``, we'll see the following.

>>> c.tables()
['table1', 'table2']

Create a new table
-----------------------------------------
Create a table instance (note, that at this step no table is created).

>>> t = c.table('table3')

Create a table with columns (``column1``, ``column2``, ``column3``).

>>> t.create('column1', 'column2', 'column3')
200

Show table columns
-----------------------------------------
>>> t.columns()
['column1', 'column2', 'column3']

Insert data into a single row
-----------------------------------------
>>> t.insert(
>>>     'my-key-1',
>>>     {
>>>         'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
>>>         'column2': {'key21': 'value 21', 'key22': 'value 22'},
>>>         'column3': {'key32': 'value 31', 'key32': 'value 32'}
>>>     }
>>> )
200

Fetch a single row with all columns
-----------------------------------------
>>> t.fetch('my-key-1')
{
    'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
    'column2': {'key21': 'value 21', 'key22': 'value 22'},
    'column3': {'key32': 'value 31', 'key32': 'value 32'}
}

Fetch a single row with selected columns
-----------------------------------------
>>> t.fetch('my-key-1', ['column1', 'column2'])
{
    'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
    'column2': {'key21': 'value 21', 'key22': 'value 22'},
}

Narrow the result set even more
-----------------------------------------
>>> t.fetch('my-key-1', {'column1': ['key11', 'key13'], 'column3': ['key32']})
{
    'column1': {'key11': 'value 11', 'key13': 'value 13'},
    'column3': {'key32': 'value 32'}
}

Add columns to the table
-----------------------------------------
Add columns given (``column4``, ``column5``).

>>> t.add_columns('column4', 'column5')

Update row data
-----------------------------------------
>>> t.update(
>>>     'my-key-1',
>>>     {'column4': {'key41': 'value 41', 'key42': 'value 42'}}
>>> )

Drop columns from table
-----------------------------------------
Drop columns given (``column4``, ``column5``).

>>> t.drop_columns('column4', 'column5')

Batch insert
-----------------------------------------
>>> data = {
>>>     'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
>>>     'column2': {'key21': 'value 21', 'key22': 'value 22'},
>>> }
>>> b = t.batch()
>>> for i in range(0, 5000):
>>>     b.insert('my-key-%s' % i, data)
>>> b.commit(finalize=True)

Batch update
-----------------------------------------
>>> data = {
>>>     'column3': {'key31': 'value 31', 'key32': 'value 32'},
>>> }
>>> b = t.batch()
>>> for i in range(0, 5000):
>>>     b.update('my-key-%s' % i, data)
>>> b.commit(finalize=True)

Fetch all rows
-----------------------------------------
Table scanning is in development. At the moment it's only possible to fetch all rows from a
table given. Results are stored in a generator.

>>> res = t.fetch_all_rows()

More examples
=========================================

Show software version
-----------------------------------------
>>> print connection.version
{u'JVM': u'Sun Microsystems Inc. 1.6.0_43-20.14-b01',
 u'Jersey': u'1.8',
 u'OS': u'Linux 3.5.0-30-generic amd64',
 u'REST': u'0.0.2',
 u'Server': u'jetty/6.1.26'}

Show cluster version
-----------------------------------------
>>> print connection.cluster_version
u'0.94.7'

Show cluster status
-----------------------------------------
>>> print connection.cluster_status
{u'DeadNodes': [],
 u'LiveNodes': [{u'Region': [{u'currentCompactedKVs': 0,
 ...
 u'regions': 3,
 u'requests': 0}

Show table schema
-----------------------------------------
>>> print table.schema()
{u'ColumnSchema': [{u'BLOCKCACHE': u'true',
   u'BLOCKSIZE': u'65536',
 ...
   u'IS_ROOT': u'false',
 u'name': u'messages'}

Print table metadata
-----------------------------------------
>>> print table.regions() # Alias of `table.regions`

License
===================================
GPL 2.0/LGPL 2.1

Support
===================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================
Artur Barseghyan <artur.barseghyan@gmail.com>

Documentation
====================================

Contents:

.. toctree::
   :maxdepth: 20

   starbase


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

