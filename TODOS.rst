====================================
TODOS
====================================
Base on MoSCoW principle. Must haves and should haves are planned to be worked on.

* Features/issues marked with plus (+) are implemented/solved.
* Features/issues marked with minus (-) are yet to be implemented.

Must haves
------------------------------------
+ Lower version of six. Get rid of PY2 checks or check for the version of six and use bundled version of
  it (1.4.1) in case if version installed is lower than the version required.
- Scanning support.
- Syntax globbing.
- Update tests. Include tests for Batch insert. Move some code parts into separate private methods which 
  are used in tests.
- Make `exists` check on the table instance optional (`on` by default, but possible to switch off (for a 
  speed up == less HTTP requests).

Should haves
------------------------------------

Could haves
------------------------------------

Would haves
------------------------------------
