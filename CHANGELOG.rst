Release history
=====================================

0.2.9
-------------------------------------
2014-03-08

- Less strict `requests` requirement (from ==1.2.3 to >= 1.2.3).

0.2.8
-------------------------------------
2014-01-30

- More on exceptions. Adding `IntegrityError` exception added. Several methods (for example `Table.create`)
  got an optional `fail_silently` argument.
- Improved documentation (mainly building of).

0.2.7
-------------------------------------
2013-12-16

- `DoesNotExist` and `ParseError` exceptions added, along with `fail_silently` argument for appropriate
  methods of the `Table`, `Batch` and `HttpRequest` classes.

0.2.6
-------------------------------------
2013-12-05

- Minor fixes.

0.2.5
-------------------------------------
2013-11-15

- Minor fixes.

0.2.4
-------------------------------------
2013-11-09

- Minor fixes.

0.2.3
-------------------------------------
2013-10-26

- Fixed HTTP basic auth.

0.2.2
-------------------------------------
2013-10-26

- Requiored version of `six` lowered to 1.1.0.
- Minor fixes.

0.2.1
-------------------------------------
2013-10-18

- Basic filtering optionsg added.

0.2
-------------------------------------
2013-09-13

- Python 2.6.8 and 3.3 support addeded.

0.1
-------------------------------------
2013-08-12

- Initial.